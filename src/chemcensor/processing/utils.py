from rdkit import Chem

from .errors.validator_errors import RxnSmilesArrowsError
from .errors.validator_errors import RxnSmilesLengthError
from .errors.validator_errors import RxnSmilesNoCarbonError
from .errors.validator_errors import RxnSmilesRDKitError
from .errors.validator_errors import RxnSmilesSyntaxError
from .fake_mapper import ATOM_MAPS_META_KEY
from chemcensor.basic.errors.molecule_errors import InvalidSMILESError


def length_check(reaction_smiles: str) -> None:
    """Check that reaction SMILES length is within the allowed range (1–512).

    :param reaction_smiles: Reaction SMILES string to check.
    :type reaction_smiles: str

    :raises RxnSmilesLengthError: If length is not between 1 and 512 characters.
    """
    if not 1 <= len(reaction_smiles) <= 512:
        raise RxnSmilesLengthError(
            msg="Reaction smiles must be 1-512 characters.",
            reaction_smiles=reaction_smiles,
        )


def syntax_check(reaction_smiles: str) -> None:
    """Check that reaction SMILES has exactly two parts separated by '>>'.

    :param reaction_smiles: Reaction SMILES string to check.
    :type reaction_smiles: str

    :raises RxnSmilesSyntaxError: If '>>' is missing or there are not exactly
            two non-empty parts.
    """
    if ">>" not in reaction_smiles:
        raise RxnSmilesSyntaxError(
            msg="Reaction smiles must contain '>>'.",
            reaction_smiles=reaction_smiles,
        )

    if len([part for part in reaction_smiles.split(">>") if part]) != 2:
        raise RxnSmilesSyntaxError(
            msg="Reaction smiles must contain " "exactly two parts separated by '>>'.",
            reaction_smiles=reaction_smiles,
        )


def check_coordinate_bonds(reaction_smiles: str) -> None:
    """Check that reaction SMILES does not contain coordinate bond arrows.

    :param reaction_smiles: Reaction SMILES string to check.
    :type reaction_smiles: str

    :raises RxnSmilesArrowsError: If '->' or '<-' (coordinate bonds) are present.
    """
    if "->" in reaction_smiles or "<-" in reaction_smiles:
        raise RxnSmilesArrowsError(
            msg="Coordinate bonds not supported.", reaction_smiles=reaction_smiles
        )


def at_least_one_carbon_check(reaction_smiles: str) -> None:
    """Check that reaction SMILES contains at least one carbon (c or C).

    :param reaction_smiles: Reaction SMILES string to check.
    :type reaction_smiles: str

    :raises RxnSmilesNoCarbonError: If neither 'c' nor 'C' appears in the string.
    """
    if "c" not in reaction_smiles and "C" not in reaction_smiles:
        raise RxnSmilesNoCarbonError(
            msg="Rxn smiles must contain at least one C",
            reaction_smiles=reaction_smiles,
        )


def validate_smiles_in_rdkit(reaction_smiles: str) -> None:
    """Validate left and right sides of reaction SMILES with RDKit.

    :param reaction_smiles: Reaction SMILES string (reagents>>products).
    :type reaction_smiles: str

    :raises RxnSmilesRDKitError: If reagents or products SMILES are invalid
            according to RDKit.
    """
    reagents, products = reaction_smiles.split(">>")
    for smiles in [reagents, products]:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise RxnSmilesRDKitError(
                msg=f"Invalid smiles: {smiles}", reaction_smiles=reaction_smiles
            )


def extract_atom_map_numbers(smiles: str):
    """Extract atom map numbers from a SMILES string.

    :param smiles: SMILES string to extract atom map numbers from.
    :type smiles: str

    :return: Dictionary of atom map numbers.
    :rtype: dict
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise InvalidSMILESError(smiles)
    # Map: rdkit index -> atom map number (only if atom map is present and > 0)
    amap = {}
    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        map_num = atom.GetAtomMapNum()
        if map_num > 0:
            amap[idx] = map_num
    return amap


def prepare_fake_mapper_meta_from_mapped_rxn(mapped_rxn_smiles: str) -> dict:
    """
    Given an atom-mapped reaction SMILES, produce the metadata dictionary
    for FakeMapper as expected in Reaction.meta.
    {
        "reactants": ( {atom_idx: map_num, ...}, ... ),
        "product": {atom_idx: map_num, ...}
    }

    :param mapped_rxn_smiles: Atom-mapped reaction SMILES.
    :type mapped_rxn_smiles: str

    :return: Metadata dictionary for FakeMapper.
    :rtype: dict

    :raises ValueError: If input is not a reaction SMILES or if SMILES is invalid.
    """

    if ">>" not in mapped_rxn_smiles:
        raise RxnSmilesSyntaxError(
            msg="Input is not a reaction SMILES: missing '>>'",
            reaction_smiles=mapped_rxn_smiles,
        )
    reactant_part, product_part = mapped_rxn_smiles.split(">>")

    reactant_frags = reactant_part.split(".") if reactant_part else []

    reactants_maps = tuple(extract_atom_map_numbers(frag) for frag in reactant_frags)
    product_map = extract_atom_map_numbers(product_part)
    return {ATOM_MAPS_META_KEY: {"reactants": reactants_maps, "product": product_map}}
