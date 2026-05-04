from dataclasses import replace
from typing import Sequence

from ..basic import Reaction
from ..basic import ReactionTransform
from ..basic.errors.molecule_errors import MoleculeError
from ..basic.errors.reaction_transform_errors import ReactionTransformError
from .base import process_batch as _process_batch
from .errors.reaction_transform_errors import ReactionTransformCreationError
from .errors.reaction_transform_errors import ReactionTransformEmptyReactionSMILESError


class TransformCreator:
    """
    Creates ReactionTransform from reaction SMILES and assigns it to the reaction.

    This processor extracts the reaction transform information and populates
    the reaction_transform field of the Reaction.
    """

    def process(self, reaction: Reaction) -> Reaction:
        """
        Create ReactionTransform from reaction SMILES and assign it to the reaction.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: Reaction with ReactionTransform
        :rtype: Reaction
        """
        if reaction.processed_reaction_smiles == "":
            raise ReactionTransformEmptyReactionSMILESError()

        try:
            reaction_transform = ReactionTransform.from_reaction_smiles(
                reaction.processed_reaction_smiles
            )
        except (ReactionTransformError, MoleculeError) as e:
            raise ReactionTransformCreationError(e) from e

        return replace(reaction, reaction_transform=reaction_transform)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Create ReactionTransform for a batch of reactions.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Batch of reactions with ReactionTransform assigned
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
