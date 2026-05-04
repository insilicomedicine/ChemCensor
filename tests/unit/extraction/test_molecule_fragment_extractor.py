import pytest
from rdkit import Chem

from chemcensor.basic import Molecule
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.configs import ExtractionConfig
from chemcensor.extraction.molecule_fragment_extractor import (
    MolecularFragmentExtractor,
)


# ============================================================================
# Helpers
# ============================================================================


def _map_to_idx(mol: Molecule, map_num: int) -> int:
    """Get atom index by atom map number."""
    for atom in mol.atom_mapped_canonical_rdmol.GetAtoms():
        if atom.GetAtomMapNum() == map_num:
            return atom.GetIdx()
    raise ValueError(f"No atom with map number {map_num}")


def _maps_to_idxs(mol: Molecule, *map_nums: int) -> list[int]:
    """Get atom indices by atom map numbers."""
    return [_map_to_idx(mol, m) for m in map_nums]


# ============================================================================
# Molecule fixtures (atom-mapped so _add_unmapped_atoms behaves correctly)
# ============================================================================


@pytest.fixture
def pentane() -> Molecule:
    """Pentane: C1-C2-C3-C4-C5 (all mapped)."""
    smiles = "[CH3:1][CH2:2][CH2:3][CH2:4][CH3:5]"
    return Molecule.from_atom_mapped_smiles(smiles)


@pytest.fixture
def toluene() -> Molecule:
    """Toluene: benzene ring (atoms :1–:6) + methyl (:7)."""
    smiles = "[cH:1]1[cH:2][cH:3][cH:4][cH:5][c:6]1[CH3:7]"
    return Molecule.from_atom_mapped_smiles(smiles)


@pytest.fixture
def naphthalene() -> Molecule:
    """Naphthalene: two fused 6-membered aromatic rings."""
    smiles = "[cH:1]1[cH:2][cH:3][c:4]2[cH:5][cH:6][cH:7][cH:8][c:9]2[cH:10]1"
    return Molecule.from_atom_mapped_smiles(smiles)


@pytest.fixture
def acetone() -> Molecule:
    """Acetone: CH3-C(=O)-CH3 — contains C=O functional group."""
    smiles = "[CH3:1][C:2](=[O:3])[CH3:4]"
    return Molecule.from_atom_mapped_smiles(smiles)


# ============================================================================
# Basic extraction
# ============================================================================


class TestExtractFragmentBasic:
    """Core contract: returns correct types, core atoms are preserved."""

    def test_returns_mol_and_list(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        frag, indices = ext.extract_fragment(pentane, _maps_to_idxs(pentane, 3))
        assert isinstance(frag, Chem.Mol)
        assert isinstance(indices, list)

    def test_core_atoms_always_included(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        core = _maps_to_idxs(pentane, 2, 4)
        _, indices = ext.extract_fragment(pentane, core)
        for idx in core:
            assert idx in indices

    def test_fragment_has_atoms(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=1)
        )
        frag, _ = ext.extract_fragment(pentane, _maps_to_idxs(pentane, 3))
        assert frag.GetNumAtoms() > 0

    def test_fragment_preserves_atom_map_numbers(self, pentane: Molecule) -> None:
        """Fragment atoms keep the same SMILES map numbers as in the parent mol."""
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=1)
        )
        parent = pentane.atom_mapped_canonical_rdmol
        frag, expanded_indices = ext.extract_fragment(
            pentane, _maps_to_idxs(pentane, 3)
        )
        assert frag.GetNumAtoms() == len(expanded_indices)
        for frag_i, parent_idx in enumerate(expanded_indices):
            assert (
                frag.GetAtomWithIdx(frag_i).GetAtomMapNum()
                == parent.GetAtomWithIdx(parent_idx).GetAtomMapNum()
            )


# ============================================================================
# Neighbor depth
# ============================================================================


class TestNeighborDepth:
    """Verify that neighbor_depth correctly expands the fragment."""

    def test_depth_zero_only_core(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        core = [2, 3]
        _, indices = ext.extract_fragment(pentane, core)
        assert set(indices) == set(core)

    def test_depth_one_adds_immediate_neighbors(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=1)
        )
        c3 = _map_to_idx(pentane, 3)
        c2 = _map_to_idx(pentane, 2)
        c4 = _map_to_idx(pentane, 4)
        _, indices = ext.extract_fragment(pentane, [c3])
        assert c2 in indices
        assert c4 in indices

    def test_depth_two_reaches_ends(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=2)
        )
        c3 = _map_to_idx(pentane, 3)
        _, indices = ext.extract_fragment(pentane, [c3])
        expected = set(_maps_to_idxs(pentane, 1, 2, 3, 4, 5))
        assert set(indices) == expected


# ============================================================================
# Ring inclusion
# ============================================================================


class TestRingInclusion:
    """Verify include_rings adds complete rings when core touches them."""

    def test_ring_atoms_included(self, toluene: Chem.Mol) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(
                center_type=ReactionCenterType.RC1,
                neighbor_depth=0,
                include_rings=True,
            )
        )
        core = _maps_to_idxs(toluene, 1)
        _, indices = ext.extract_fragment(toluene, core)
        ring_atoms = set(_maps_to_idxs(toluene, 1, 2, 3, 4, 5, 6))
        assert ring_atoms.issubset(set(indices))

    def test_no_ring_expansion_when_disabled(self, toluene: Chem.Mol) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        # Core is the methyl — not in the ring
        core = _maps_to_idxs(toluene, 7)
        _, indices = ext.extract_fragment(toluene, core)
        ring_only = set(_maps_to_idxs(toluene, 1, 2, 3, 4, 5))
        assert not ring_only.intersection(set(indices))


# ============================================================================
# Fused ring systems
# ============================================================================


class TestFusedRings:
    """Verify include_fused expands to the full fused system."""

    def test_fused_system_fully_included(self, naphthalene: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(
                center_type=ReactionCenterType.RC1,
                neighbor_depth=0,
                include_rings=True,
                include_fused=True,
            )
        )
        core = _maps_to_idxs(naphthalene, 1)
        _, indices = ext.extract_fragment(naphthalene, core)
        all_atoms = set(_maps_to_idxs(naphthalene, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        assert all_atoms.issubset(set(indices))

    def test_only_one_ring_without_fused(self, naphthalene: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(
                center_type=ReactionCenterType.RC1,
                neighbor_depth=0,
                include_rings=True,
            )
        )
        core = _maps_to_idxs(naphthalene, 1)
        _, indices = ext.extract_fragment(naphthalene, core)
        # Only one ring (6 atoms) — not all 10
        assert len(indices) < 10


# ============================================================================
# Substituents
# ============================================================================


class TestSubstituents:
    """Verify include_substituents adds non-ring neighbors of aromatic atoms."""

    def test_substituent_included(self, toluene: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(
                center_type=ReactionCenterType.RC1,
                neighbor_depth=0,
                include_rings=True,
                include_substituents=True,
            )
        )
        core = _maps_to_idxs(toluene, 1)
        _, indices = ext.extract_fragment(toluene, core)
        ch3 = _map_to_idx(toluene, 7)
        assert ch3 in indices

    def test_no_substituent_when_disabled(self, toluene: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(
                center_type=ReactionCenterType.RC1,
                neighbor_depth=0,
                include_rings=True,
            )
        )
        core = _maps_to_idxs(toluene, 1)
        _, indices = ext.extract_fragment(toluene, core)
        ch3 = _map_to_idx(toluene, 7)
        assert ch3 not in indices


# ============================================================================
# Functional group expansion
# ============================================================================


class TestFunctionalGroupExpansion:
    """Verify that FG patterns expand atoms (e.g. C=O adds O)."""

    def test_carbonyl_oxygen_expanded(self, acetone: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        c_idx = _map_to_idx(acetone, 2)  # carbonyl carbon
        o_idx = _map_to_idx(acetone, 3)  # carbonyl oxygen
        _, indices = ext.extract_fragment(acetone, [c_idx])
        assert o_idx in indices

    def test_carbonyl_carbon_expanded(self, acetone: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        o_idx = _map_to_idx(acetone, 3)  # carbonyl oxygen
        c_idx = _map_to_idx(acetone, 2)  # carbonyl carbon
        _, indices = ext.extract_fragment(acetone, [o_idx])
        assert c_idx in indices


# ============================================================================
# State isolation between calls
# ============================================================================


class TestStateReset:
    """Successive extract_fragment calls must be independent."""

    def test_no_state_leakage(self, pentane: Molecule, toluene: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=0)
        )
        # First call on pentane
        core1 = _maps_to_idxs(pentane, 3)
        _, indices1 = ext.extract_fragment(pentane, core1)

        # Second call on toluene — different molecule, different core
        core2 = _maps_to_idxs(toluene, 7)
        _, indices2 = ext.extract_fragment(toluene, core2)

        assert set(indices1) != set(indices2)
        assert set(indices2) == set(core2)

    def test_repeated_same_call_stable(self, pentane: Molecule) -> None:
        ext = MolecularFragmentExtractor(
            ExtractionConfig(center_type=ReactionCenterType.RC1, neighbor_depth=1)
        )
        core = _maps_to_idxs(pentane, 3)
        _, indices_a = ext.extract_fragment(pentane, core)
        _, indices_b = ext.extract_fragment(pentane, core)
        assert indices_a == indices_b
