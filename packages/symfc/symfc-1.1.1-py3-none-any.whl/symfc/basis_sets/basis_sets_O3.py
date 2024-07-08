"""Symmetry adapted basis sets of 3rd order force constants."""

from __future__ import annotations

import time
from typing import Optional, Union

import numpy as np
from scipy.sparse import coo_array, csr_array

from symfc.spg_reps import SpgRepsO3
from symfc.utils.cutoff_tools import FCCutoff
from symfc.utils.eig_tools import (
    dot_product_sparse,
    eigsh_projector,
    eigsh_projector_sumrule,
)
from symfc.utils.matrix_tools_O3 import (
    compressed_projector_sum_rules_O3,
    projector_permutation_lat_trans_O3,
)
from symfc.utils.utils import SymfcAtoms
from symfc.utils.utils_O3 import (
    get_atomic_lat_trans_decompr_indices_O3,
    get_compr_coset_projector_O3,
    get_lat_trans_compr_matrix_O3,
)

from . import FCBasisSetBase


def print_sp_matrix_size(c: Union[csr_array, coo_array], header: str):
    """Show sparse matrix size."""
    print(header, c.shape, len(c.data), flush=True)


class FCBasisSetO3(FCBasisSetBase):
    """Symmetry adapted basis set for 3rd order force constants.

    Attributes
    ----------
    basis_set : ndarray
        Compressed force constants basis set.
        shape=(n_a * N * 9, n_bases), dtype='double'
    full_basis_set : ndarray
        Full (decompressed) force constants basis set.
        shape=(N * N * 9, n_bases), dtype='double'
    decompression_indices : ndarray
        Decompression indices in (N,N,3,3) order.
        shape=(N^2*9,), dtype='int_'.
    compresssion_indices : ndarray
        Compression indices in (n_a,N,3,3) order.
        shape=(n_a*N*9, n_lp), dtype='int_'.
    translation_permutations : ndarray
        Atom indices after lattice translations.
        shape=(lattice_translations, supercell_atoms), dtype=int.

    """

    def __init__(
        self,
        supercell: SymfcAtoms,
        cutoff: float = None,
        spacegroup_operations: Optional[dict] = None,
        use_mkl: bool = False,
        log_level: int = 0,
    ):
        """Init method.

        Parameters
        ----------
        supercell : SymfcAtoms
            Supercell.
        spacegroup_operations : dict, optional
            Space group operations in supercell, by default None. When None,
            spglib is used. The following keys and values correspond to spglib
            symmetry dataset:
                rotations : array_like
                translations : array_like
        log_level : int, optional
            Log level. Default is 0.

        """
        super().__init__(supercell, use_mkl=use_mkl, log_level=log_level)
        self._spg_reps = SpgRepsO3(
            supercell, spacegroup_operations=spacegroup_operations
        )
        if cutoff is None:
            self._fc_cutoff = None
        else:
            self._fc_cutoff = FCCutoff(supercell, cutoff=cutoff)

        trans_perms = self._spg_reps.translation_permutations
        self._atomic_decompr_idx = get_atomic_lat_trans_decompr_indices_O3(trans_perms)

    @property
    def basis_set(self) -> Optional[csr_array]:
        """Return compressed basis set.

        n_c = len(compressed_indices).

        shape=(n_c*N*N*3*3*3, n_bases), dtype='double'.

        Data in first dimension is ordered by (n_c,N,N,3,3,3).

        """
        return self._basis_set

    @property
    def compression_matrix(self) -> Optional[csr_array]:
        """Return compression matrix.

        This expands fc basis_sets to (N*N*N*3*3*3, n_bases).

        """
        trans_perms = self._spg_reps.translation_permutations
        c_trans = get_lat_trans_compr_matrix_O3(trans_perms)
        return dot_product_sparse(
            c_trans, self._n_a_compression_matrix, use_mkl=self._use_mkl
        )

    @property
    def compact_compression_matrix(self) -> Optional[csr_array]:
        """Return compact compression matrix.

        This expands basis_sets to (n_a*N*N*3*3*3, n_bases).

        """
        n_lp = self.translation_permutations.shape[0]
        return self._n_a_compression_matrix / np.sqrt(n_lp)

    @property
    def atomic_decompr_idx(self) -> np.ndarray:
        """Return atomic permutation."""
        return self._atomic_decompr_idx

    def run(self) -> FCBasisSetO3:
        """Compute compressed force constants basis set."""
        trans_perms = self._spg_reps.translation_permutations

        tt0 = time.time()
        proj_pt = projector_permutation_lat_trans_O3(
            trans_perms,
            atomic_decompr_idx=self._atomic_decompr_idx,
            fc_cutoff=self._fc_cutoff,
            use_mkl=self._use_mkl,
            verbose=self._log_level > 0,
        )
        tt1 = time.time()

        c_pt = eigsh_projector(proj_pt, verbose=self._log_level > 0)
        if self._log_level:
            print(" c_pt (size) :", c_pt.shape, flush=True)
        tt2 = time.time()

        proj_rpt = get_compr_coset_projector_O3(
            self._spg_reps,
            fc_cutoff=self._fc_cutoff,
            atomic_decompr_idx=self._atomic_decompr_idx,
            c_pt=c_pt,
            verbose=self._log_level > 0,
        )
        tt3 = time.time()

        c_rpt = eigsh_projector(proj_rpt, verbose=self._log_level > 0)
        if self._log_level:
            print(" c_rpt (size) :", c_rpt.shape, flush=True)
        tt4 = time.time()

        n_a_compress_mat = dot_product_sparse(c_pt, c_rpt, use_mkl=self._use_mkl)
        tt5 = time.time()

        proj = compressed_projector_sum_rules_O3(
            trans_perms,
            n_a_compress_mat,
            atomic_decompr_idx=self._atomic_decompr_idx,
            fc_cutoff=self._fc_cutoff,
            use_mkl=self._use_mkl,
            verbose=self._log_level > 0,
        )
        tt6 = time.time()
        eigvecs = eigsh_projector_sumrule(proj, verbose=self._log_level > 0)

        if self._log_level:
            print("Final size of basis set:", eigvecs.shape, flush=True)
        tt7 = time.time()

        if self._log_level:
            print(
                "Time (proj(perm @ lattice trans.)  :",
                "{:.3f}".format(tt1 - tt0),
                flush=True,
            )
            print(
                "Time (eigh(perm @ ltrans))         :",
                "{:.3f}".format(tt2 - tt1),
                flush=True,
            )
            print(
                "Time (coset)                       :",
                "{:.3f}".format(tt3 - tt2),
                flush=True,
            )
            print(
                "Time (eigh(coset @ perm @ ltrans)) :",
                "{:.3f}".format(tt4 - tt3),
                flush=True,
            )
            print(
                "Time (c_pt @ c_rpt)                :",
                "{:.3f}".format(tt5 - tt4),
                flush=True,
            )
            print(
                "Time (proj(sum))                   :",
                "{:.3f}".format(tt6 - tt5),
                flush=True,
            )
            print(
                "Time (eigh(sum))                   :",
                "{:.3f}".format(tt7 - tt6),
                flush=True,
            )
            print("---", flush=True)
            print(
                "Time (Basis FC3)                   :",
                "{:.3f}".format(tt7 - tt0),
                flush=True,
            )

        self._basis_set = eigvecs
        self._n_a_compression_matrix = n_a_compress_mat

        return self
