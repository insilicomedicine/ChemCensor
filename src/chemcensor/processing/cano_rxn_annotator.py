from dataclasses import replace
from typing import Sequence

from rdkit import Chem

from ..basic import Reaction
from ..basic import ReactionTransform
from .base import process_batch as _process_batch
from .errors.cano_rxn_annotator_errors import CanoRxnAnnotatorEmptyTransformError


class CanoRxnAnnotator:
    """Annotates a reaction with its canonical SMILES.

    Builds the canonical reaction SMILES from the canonical SMILES
    already stored in the transform's Molecule objects
    (reactants and product).
    """

    @staticmethod
    def _build_canonical_smiles(transform: ReactionTransform) -> str:
        """Build canonical reaction SMILES from a ReactionTransform.

        :param transform: The reaction transform containing Molecule objects.
        :type transform: ReactionTransform
        :return: Canonical reaction SMILES in ``R1.R2>>P`` format.
        :rtype: str
        """
        reactants_smiles = ".".join(r.canonical_smiles for r in transform.reactants)
        # canonicalize the reactants order
        reactants_smiles = Chem.MolToSmiles(Chem.MolFromSmiles(reactants_smiles))
        return f"{reactants_smiles}>>{transform.product.canonical_smiles}"

    def process(self, reaction: Reaction) -> Reaction:
        """Annotate a reaction with its canonical SMILES.

        :param reaction: Reaction to process.
        :type reaction: Reaction
        :return: Reaction with ``canonical_smiles`` populated.
        :rtype: Reaction
        """
        if reaction.reaction_transform is None:
            raise CanoRxnAnnotatorEmptyTransformError()

        canonical_smiles = self._build_canonical_smiles(reaction.reaction_transform)
        return replace(reaction, canonical_smiles=canonical_smiles)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Annotate a batch of reactions with canonical SMILES.

        :param reactions: Batch of reactions to process.
        :type reactions: Sequence[Reaction]
        :return: Batch of annotated reactions.
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
