import re
from dataclasses import replace
from typing import Sequence

from ..basic import Reaction
from .base import process_batch as _process_batch
from .errors.orphan_remover_errors import MultipleMappedProductsError
from .errors.orphan_remover_errors import NoMappedProductError
from .errors.orphan_remover_errors import NoMappedReactantsError
from .errors.orphan_remover_errors import ReactionNotSplitError

# Pattern to match atom mappings in SMILES: [C:1], [N:2], etc.
ATOM_MAPPING_PATTERN = re.compile(r"\[.*?:\d+\]")


def _has_atom_mapping(smiles: str) -> bool:
    """Check if a SMILES fragment contains atom mappings."""
    return ATOM_MAPPING_PATTERN.search(smiles) is not None


class OrphanRemover:
    """Removes orphan chemicals and spectators from reactions.

    Orphans are fragments without atom mapping.
    Spectators are identically mapped fragments present on both sides.
    """

    def process(self, reaction: Reaction) -> Reaction:
        """
        Remove orphan and spectator fragments from a mapped reaction.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: Reaction with orphans and spectators removed
        :rtype: Reaction
        """
        if ">>" not in reaction.mapped_reaction_smiles:
            raise ReactionNotSplitError(reaction.mapped_reaction_smiles)

        reactants_str, products_str = reaction.mapped_reaction_smiles.split(
            ">>", maxsplit=1
        )

        reactant_list = reactants_str.split(".")
        product_list = products_str.split(".")

        # Step 1: keep only mapped fragments (remove orphans)
        mapped_reactants = [r for r in reactant_list if _has_atom_mapping(r)]
        mapped_products = [p for p in product_list if _has_atom_mapping(p)]

        # Step 2: remove spectators (identical fragments on both sides)
        spectator_smiles = set(mapped_reactants) & set(mapped_products)
        filtered_reactants = [r for r in mapped_reactants if r not in spectator_smiles]
        filtered_products = [p for p in mapped_products if p not in spectator_smiles]

        # Validate
        if not filtered_products:
            raise NoMappedProductError(reaction.mapped_reaction_smiles)
        if len(filtered_products) > 1:
            raise MultipleMappedProductsError(reaction.mapped_reaction_smiles)
        if not filtered_reactants:
            raise NoMappedReactantsError(reaction.mapped_reaction_smiles)

        # Reconstruct reaction SMILES
        new_mapped = f"{'.'.join(filtered_reactants)}>>{filtered_products[0]}"

        return replace(reaction, processed_reaction_smiles=new_mapped)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Remove orphans and spectators from a batch of reactions.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Processed batch of reactions
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
