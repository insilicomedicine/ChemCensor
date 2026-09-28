import re

from frozendict import frozendict
from rdkit import Chem

from ..basic import Reaction
from ..basic.errors.molecule_errors import InvalidSMILESError
from .errors.mapper_errors import MapperError
from .errors.validator_errors import RxnSmilesArrowsError
from .errors.validator_errors import RxnSmilesLengthError
from .errors.validator_errors import RxnSmilesNoCarbonError
from .errors.validator_errors import RxnSmilesRDKitError
from .errors.validator_errors import RxnSmilesSyntaxError
from .fake_mapper import ATOM_MAPS_META_KEY


_ATOM_MAP_LABEL_RE = re.compile(r":\d+(?=[\]])")


def strip_atom_map_labels(smiles: str) -> str:
    """Strip atom-map labels textually while preserving atom order.

    Textual removal is required before :class:`FakeMapper` re-attaches maps by
    atom index; RDKit canonicalization could reorder atoms.

    :param smiles: SMILES or reaction SMILES with atom-map labels.
    :type smiles: str

    :return: Input with ``:N`` labels removed from bracket atoms.
    :rtype: str
    """
    return _ATOM_MAP_LABEL_RE.sub("", smiles)


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

    Reactant atom maps whose map numbers do not appear on the product side are
    dropped. Leaving-group atoms that only exist on the reactant would otherwise
    stay mapped through FakeMapper and diverge from mappings that omit those
    labels (OrphanRemover only drops whole unmapped fragments).

    :param mapped_rxn_smiles: Atom-mapped reaction SMILES.
    :type mapped_rxn_smiles: str

    :return: Metadata dictionary for FakeMapper.
    :rtype: dict

    :raises RxnSmilesSyntaxError: If input is not a reaction SMILES.
    :raises InvalidSMILESError: If a reactant or product fragment is invalid.
    """

    if ">>" not in mapped_rxn_smiles:
        raise RxnSmilesSyntaxError(
            msg="Input is not a reaction SMILES: missing '>>'",
            reaction_smiles=mapped_rxn_smiles,
        )
    reactant_part, product_part = mapped_rxn_smiles.split(">>")

    reactant_frags = reactant_part.split(".") if reactant_part else []

    product_map = extract_atom_map_numbers(product_part)
    product_map_nums = set(product_map.values())
    reactants_maps = tuple(
        {
            idx: map_num
            for idx, map_num in extract_atom_map_numbers(frag).items()
            if map_num in product_map_nums
        }
        for frag in reactant_frags
    )
    return {ATOM_MAPS_META_KEY: {"reactants": reactants_maps, "product": product_map}}


def reaction_from_precomputed_mapping(mapped_rxn_smiles: str) -> Reaction:
    """Build a FakeMapper input reaction from atom-mapped reaction SMILES.

    Shared by process-based and in-process batch mapping so both paths parse
    precomputed mappings identically.

    :param mapped_rxn_smiles: Atom-mapped reaction SMILES.
    :type mapped_rxn_smiles: str
    :return: Unmapped reaction plus atom maps in ``Reaction.meta``.
    :rtype: Reaction
    :raises ProcessingError: If the mapping cannot be prepared.
    """
    raw_smiles = strip_atom_map_labels(mapped_rxn_smiles)
    try:
        meta = prepare_fake_mapper_meta_from_mapped_rxn(mapped_rxn_smiles)
    except InvalidSMILESError as error:
        raise MapperError(
            reaction_smiles=mapped_rxn_smiles,
            msg=str(error),
        ) from error
    return Reaction(
        reaction_smiles=raw_smiles,
        meta=frozendict(meta),
    )
