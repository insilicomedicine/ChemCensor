from rdkit import Chem

from .errors.validator_errors import RxnSmilesArrowsError
from .errors.validator_errors import RxnSmilesLengthError
from .errors.validator_errors import RxnSmilesNoCarbonError
from .errors.validator_errors import RxnSmilesRDKitError
from .errors.validator_errors import RxnSmilesSyntaxError


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
