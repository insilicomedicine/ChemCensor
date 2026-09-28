import pytest
from rdkit import Chem

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionTransform
from chemcensor.processing.errors.skeleton_conservation_validator_errors import (
    SkeletonConservationValidatorEmptyTransformError,
)
from chemcensor.processing.errors.skeleton_conservation_validator_errors import (
    SkeletonConservationValidatorTruncatedCarbonChainError,
)
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.processing.skeleton_conservation_validator import (
    find_truncated_carbon_fragments,
)
from chemcensor.processing.skeleton_conservation_validator import (
    SkeletonConservationValidator,
)


# =============================================================================
# find_truncated_carbon_fragments
# =============================================================================


def test_find_flags_terminal_carbon_attached_to_carbon():
    """A pure-carbon fragment attached to the skeleton via a C-C bond is flagged."""
    # CCOC: 0=CH3 (ethyl terminal), 1=CH2, 2=O, 3=CH3
    mol = Chem.MolFromSmiles("CCOC")
    fragments = find_truncated_carbon_fragments(mol, [0], max_fragment_size=3)
    assert fragments == [frozenset({0})]


def test_find_ignores_carbon_attached_only_to_heteroatom():
    """A carbon attached only through a heteroatom (O-/N-dealkylation) is ignored."""
    # COC: 0=CH3, 1=O, 2=CH3 -> the unmapped methyl is attached only to O
    mol = Chem.MolFromSmiles("COC")
    fragments = find_truncated_carbon_fragments(mol, [0], max_fragment_size=3)
    assert fragments == []


def test_find_ignores_fragment_containing_heteroatom():
    """A fragment that is not pure hydrocarbon (e.g. an ester leaving group) is
    ignored."""
    # CC(=O)OC: unmapped acetate-like fragment contains oxygens
    mol = Chem.MolFromSmiles("CC(=O)OC")
    fragments = find_truncated_carbon_fragments(
        mol, [0, 1, 2, 3], max_fragment_size=None
    )
    assert fragments == []


def test_find_ignores_standalone_component():
    """A fully unmapped molecule (spectator/reagent) has no skeleton attachment."""
    mol = Chem.MolFromSmiles("CC")
    fragments = find_truncated_carbon_fragments(mol, [0, 1], max_fragment_size=None)
    assert fragments == []


def test_find_respects_max_fragment_size():
    """The size cap excludes larger pure-carbon fragments."""
    # CCCCOC: 0,1,2 = propyl carbons attached to 3=CH2-O; unmapped propyl (size 3)
    mol = Chem.MolFromSmiles("CCCCOC")
    assert find_truncated_carbon_fragments(mol, [0, 1, 2], max_fragment_size=2) == []
    assert find_truncated_carbon_fragments(mol, [0, 1, 2], max_fragment_size=3) == [
        frozenset({0, 1, 2})
    ]


def test_find_ignores_terminal_methylene_double_bond():
    """A single unmapped carbon double-bonded to the skeleton (=CH2) is ignored.

    Oxidative cleavage of a terminal alkene leaves exactly this fragment; it is
    not silent homolog drift across a C-C single bond.
    """
    # C=C(c1ccccc1)CBr: atom 0 is the terminal =CH2, double-bonded to atom 1.
    mol = Chem.MolFromSmiles("C=C(c1ccccc1)CBr")
    assert find_truncated_carbon_fragments(mol, [0], max_fragment_size=None) == []


def test_find_ignores_exocyclic_methylene_double_bond():
    """An exocyclic =CH2 lost across a ring C=C is ignored (same exemption)."""
    # C=C1CN(C(=O)OC(C)(C)C)CC1F: atom 0 is the exocyclic methylene.
    mol = Chem.MolFromSmiles("C=C1CN(C(=O)OC(C)(C)C)CC1F")
    assert find_truncated_carbon_fragments(mol, [0], max_fragment_size=None) == []


# =============================================================================
# SkeletonConservationValidator (transform-level)
# =============================================================================


def _reaction_with_transform(mapped_smiles: str) -> Reaction:
    return Reaction(
        reaction_smiles=mapped_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(mapped_smiles),
    )


def test_validator_raises_without_transform():
    validator = SkeletonConservationValidator()
    with pytest.raises(SkeletonConservationValidatorEmptyTransformError):
        validator.process(Reaction(reaction_smiles=""))


def test_validator_flags_ethyl_to_methyl_deletion():
    """Ethyl ether silently truncated to a methyl ether is rejected."""
    # O-CH2 (:3) maps to O-CH3 (:3); the terminal ethyl carbon is unmapped.
    reaction = _reaction_with_transform("[CH3:1][O:2][CH2:3]C>>[CH3:1][O:2][CH3:3]")
    validator = SkeletonConservationValidator()
    with pytest.raises(SkeletonConservationValidatorTruncatedCarbonChainError):
        validator.process(reaction)


def test_validator_passes_terminal_methylene_oxidative_cleavage():
    """C=C → C=O loss of a terminal =CH2 is legitimate and must pass."""
    # CM-3577: styrene-like oxidative cleavage; =[CH2:11] has no product map.
    reaction = _reaction_with_transform(
        "[C:2]([CH2:3][Br:4])([c:5]1ccccc1)=[CH2:11].O=[O:1]"
        ">>[O:1]=[C:2]([CH2:3][Br:4])[c:5]1ccccc1"
    )
    validator = SkeletonConservationValidator()
    assert validator.process(reaction) is reaction


def test_validator_passes_exocyclic_methylene_oxidative_cleavage():
    """Exocyclic =CH2 → ring ketone must not be flagged as homolog drift."""
    reaction = _reaction_with_transform(
        "[CH2:99]=[C:1]1[CH2:2][N:3]([C:4](=[O:5])[O:6][C:7]"
        "([CH3:8])([CH3:9])[CH3:10])[CH2:11][CH:12]1[F:13]"
        ">>[C:1]1(=[O:14])[CH2:2][N:3]([C:4](=[O:5])[O:6][C:7]"
        "([CH3:8])([CH3:9])[CH3:10])[CH2:11][CH:12]1[F:13]"
    )
    validator = SkeletonConservationValidator()
    assert validator.process(reaction) is reaction


def test_validator_passes_ring_closing_metathesis():
    """RCM loses two terminal =CH2 (ethylene); both must be exempted.

    CM-3577: the unmapped methylenes are double-bonded to the retained skeleton,
    not silent C-C homolog drift.
    """
    reaction = _reaction_with_transform(
        "[O:1]=[C:2]([O:3][CH2:4][c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1)"
        "[N:11]([CH2:12][CH:13]=[CH2:29])"
        "[CH:18]([CH2:17][CH2:16][CH2:15][CH:14]=[CH2:28])"
        "[CH2:19][O:20][CH2:21][c:22]1[cH:23][cH:24][cH:25][cH:26][cH:27]1"
        ">>"
        "[O:1]=[C:2]([O:3][CH2:4][c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1)"
        "[N:11]1[CH2:12][CH:13]=[CH:14][CH2:15][CH2:16][CH2:17][CH:18]1"
        "[CH2:19][O:20][CH2:21][c:22]1[cH:23][cH:24][cH:25][cH:26][cH:27]1"
    )
    validator = SkeletonConservationValidator()
    assert validator.process(reaction) is reaction


def test_validator_passes_o_demethylation():
    """O-demethylation breaks a C-O bond, so it is not flagged."""
    reaction = _reaction_with_transform("C[O:1][CH3:2]>>[OH:1][CH3:2]")
    validator = SkeletonConservationValidator()
    assert validator.process(reaction) is reaction


def test_validator_ignores_carbon_addition_by_default():
    """A product-side carbon addition across a C-C bond is not flagged by default."""
    # Reverse of the truncation: methyl -> ethyl (carbon appears on product side).
    reaction = _reaction_with_transform("[CH3:1][O:2][CH3:3]>>[CH3:1][O:2][CH2:3]C")
    validator = SkeletonConservationValidator()
    assert validator.process(reaction) is reaction


def test_validator_flags_carbon_addition_when_enabled():
    """With check_additions, a product-side carbon addition is flagged."""
    reaction = _reaction_with_transform("[CH3:1][O:2][CH3:3]>>[CH3:1][O:2][CH2:3]C")
    validator = SkeletonConservationValidator(check_additions=True)
    with pytest.raises(SkeletonConservationValidatorTruncatedCarbonChainError):
        validator.process(reaction)


def test_validator_error_contains_reaction_smiles():
    mapped = "[CH3:1][O:2][CH2:3]C>>[CH3:1][O:2][CH3:3]"
    reaction = _reaction_with_transform(mapped)
    validator = SkeletonConservationValidator()
    with pytest.raises(
        SkeletonConservationValidatorTruncatedCarbonChainError
    ) as exc_info:
        validator.process(reaction)
    assert mapped in str(exc_info.value)
    assert exc_info.value.reaction_smiles == mapped
    assert exc_info.value.side == "reactant"


# =============================================================================
# Full pipeline (real mapper)
# =============================================================================


def test_pipeline_rejects_ethyl_to_methyl_artifact():
    """The Boc-removal record that also silently turns an ethyl ether into a
    methyl ether is rejected by the pipeline."""
    reaction_smiles = (
        "CCOCC1(Nc2nc(C)c(-c3nc(C)nc4sccc34)c([C@@H]3CCCN3C(=O)OC(C)(C)C)n2)CCCC1"
        ">>"
        "COCC1(Nc2nc(C)c(-c3nc(C)nc4sccc34)c([C@@H]3CCCN3)n2)CCCC1"
    )
    with pytest.raises(SkeletonConservationValidatorTruncatedCarbonChainError):
        ReactionProcessor().process(Reaction(reaction_smiles=reaction_smiles))


REACTION_SMILES_WITH_CONSERVED_SKELETON: tuple[str, ...] = (
    # O-demethylation: C-O bond cleavage, not flagged.
    "COc1ccccc1>>Oc1ccccc1",
    # N-deethylation: C-N bond cleavage, not flagged.
    "CCN(CC)c1ccccc1>>CCNc1ccccc1",
    # Boc removal: the leaving group contains heteroatoms.
    "CC(C)(C)OC(=O)NCCN>>NCCN",
    # Transesterification with the incoming alcohol supplied as a reactant. The
    # ester alkyl group changes (methyl -> ethyl), but the new ethyl is sourced
    # from the added ethanol and the leaving methyl departs as part of a C-O
    # (methoxy) fragment, so no pure-hydrocarbon C-C truncation is seen.
    "COC(=O)c1ccccc1.CCO>>CCOC(=O)c1ccccc1",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_CONSERVED_SKELETON,
)
def test_pipeline_passes_legitimate_dealkylations(reaction_smiles: str):
    processed = ReactionProcessor().process(Reaction(reaction_smiles=reaction_smiles))
    assert processed.dummy is False


# Allylic bromide -> allylic alcohol substitution. The mapper sources the new
# hydroxyl oxygen from methanol, leaving the methanol carbon unmapped. That lost
# carbon is attached through oxygen (C-O), not carbon, so it is a
# dealkylation-style loss the validator must ignore rather than a silent
# carbon-chain (C-C) truncation.
METHANOL_OXYGEN_DONOR_RXN_SMILES = (
    "CC(C)=O.CO.F[B-](F)(F)F.O."
    "O=C(O)CCCCCCCCC1=CC(Br)CC1=O.[Ag+].[Br-].[K+]"
    ">>O=C(O)CCCCCCCCC1=CC(O)CC1=O"
)


def test_pipeline_passes_carbon_lost_through_oxygen():
    """A methanol methyl lost across a C-O bond is not a C-C truncation."""
    reaction = Reaction(reaction_smiles=METHANOL_OXYGEN_DONOR_RXN_SMILES)
    processed = ReactionProcessor().process(reaction)
    assert processed.dummy is False
    # The validator specifically must not flag the oxygen-attached carbon loss.
    assert SkeletonConservationValidator().process(processed) is processed
