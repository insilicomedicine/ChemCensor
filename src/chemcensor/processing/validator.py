from dataclasses import replace
from typing import Callable
from typing import Sequence

from ..basic import Reaction
from .base import process_batch as _process_batch
from .errors.validator_errors import RxnSmilesArrowsError
from .errors.validator_errors import RxnSmilesLengthError
from .errors.validator_errors import RxnSmilesNoCarbonError
from .errors.validator_errors import RxnSmilesRDKitError
from .errors.validator_errors import RxnSmilesSyntaxError
from .errors.validator_errors import ValidationError
from .utils import at_least_one_carbon_check
from .utils import check_coordinate_bonds
from .utils import length_check
from .utils import syntax_check
from .utils import validate_smiles_in_rdkit

# Validators applied regardless of input length. The ``length_check`` exists
# only to keep inputs within the atom-mapper's (rxnmapper) limits; pipelines
# that map elsewhere (e.g. FakeMapper reusing precomputed maps) can drop it.
_VALIDATORS_WITHOUT_LENGTH: Sequence[Callable[[str], None]] = (
    syntax_check,
    check_coordinate_bonds,
    at_least_one_carbon_check,
    validate_smiles_in_rdkit,
)

DEFAULT_VALIDATORS: Sequence[Callable[[str], None]] = (
    length_check,
    *_VALIDATORS_WITHOUT_LENGTH,
)


class Validator:
    """Reaction SMILES validator called before any other processors."""

    validators: Sequence[Callable[[str], None]]

    def __init__(
        self,
        validators: Sequence[Callable[[str], None]] | None = None,
        *,
        check_length: bool = True,
    ) -> None:
        """
        Initialize Validator with validators.

        :param validators: Explicit validators to use; when ``None`` (default)
            a standard set is used, with or without the length check depending
            on ``check_length``.
        :type validators: Sequence[Callable[[str], None]] | None
        :param check_length: When ``True`` (default) enforce the 1-512 char
            reaction-SMILES limit. Set ``False`` when the atom mapping is
            precomputed (FakeMapper) so oversized reactions are not rejected.
            Ignored when ``validators`` is provided explicitly.
        :type check_length: bool
        """
        if validators is None:
            validators = (
                DEFAULT_VALIDATORS if check_length else _VALIDATORS_WITHOUT_LENGTH
            )
        self.validators = validators or DEFAULT_VALIDATORS

    def process(self, reaction: Reaction) -> Reaction:
        """Run all validation checks on a reaction; normalize and return it.

        Strips leading/trailing whitespace from reaction_smiles, then runs
        length, syntax, coordinate bonds, carbon, and RDKit checks.

        :param reaction: Reaction to validate.
        :type reaction: Reaction

        :return: Processed reaction after applying all validators.
        :rtype: Reaction
        """
        reaction_smiles = reaction.reaction_smiles.strip()
        if reaction_smiles != reaction.reaction_smiles:
            reaction = replace(reaction, reaction_smiles=reaction_smiles)

        try:
            for validator in self.validators:
                validator(reaction_smiles)
        except RxnSmilesLengthError as e:
            raise ValidationError(
                msg=e.msg,
                reaction_smiles=reaction_smiles,
            ) from e
        except RxnSmilesSyntaxError as e:
            raise ValidationError(
                msg=e.msg,
                reaction_smiles=reaction_smiles,
            ) from e
        except RxnSmilesArrowsError as e:
            raise ValidationError(
                msg=e.msg,
                reaction_smiles=reaction_smiles,
            ) from e
        except RxnSmilesNoCarbonError as e:
            raise ValidationError(
                msg=e.msg,
                reaction_smiles=reaction_smiles,
            ) from e
        except RxnSmilesRDKitError as e:
            raise ValidationError(
                msg=e.msg,
                reaction_smiles=reaction_smiles,
            ) from e

        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Validate batch of reactions.

        :param reactions: Batch of reactions to validate
        :type reactions: Sequence[Reaction]

        :return: Validated batch of reactions
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
