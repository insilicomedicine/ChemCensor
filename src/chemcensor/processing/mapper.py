import os
from dataclasses import replace
from typing import Sequence

from rxnmapper import BatchedMapper

from ..basic import Reaction
from ..basic import SENTINEL
from .errors.mapper_errors import JobSpecificationError
from .errors.mapper_errors import MapperError


class Mapper:
    """Mapper implementation for reaction mapping."""

    def __init__(self, batch_size: int = 1, n_jobs: int = 1) -> None:
        """Initialize Mapper.

        :param batch_size: Batch size for mapping.
        :type batch_size: int
        :param n_jobs: Number of jobs for mapping.
        :type n_jobs: int
        """
        if n_jobs < 1:
            raise JobSpecificationError(msg="n_jobs must be greater than 0")

        os.environ["OMP_NUM_THREADS"] = str(n_jobs)
        self._mapper = BatchedMapper(canonicalize=True, batch_size=batch_size)

    def _map_reaction_smiles(self, reaction_smiles: str) -> str:
        """
        Maps a reaction SMILES string to its atom-mapped counterpart
        using the  BatchedMapper (from rxnmapper package).

        :param reaction_smiles: The input reaction SMILES string to be mapped.
        :type reaction_smiles: str

        :raises MapperError: If mapping fails or
        RXNMapper returns >> placeholder.

        :return: Atom-mapped reaction SMILES string.
        :rtype: str
        """
        try:
            mapped_reaction_smiles = next(self._mapper.map_reactions([reaction_smiles]))
        except Exception as e:
            raise MapperError(reaction_smiles=reaction_smiles, msg=str(e)) from e

        if mapped_reaction_smiles == ">>":
            raise MapperError(
                reaction_smiles=reaction_smiles,
                msg="RXNMapper returned empty or invalid reaction SMILES",
            )

        return mapped_reaction_smiles

    def process(self, reaction: Reaction) -> Reaction:
        """
        Process a Reaction object and return a new Reaction
        object with the mapped_reaction_smiles field.

        :param reaction: The Reaction object with the reaction SMILES to be mapped.
        :type reaction: Reaction

        :return: A new Reaction object with the mapped_reaction_smiles field.
        :rtype: Reaction
        """
        mapped_reaction_smiles = self._map_reaction_smiles(reaction.reaction_smiles)
        return replace(reaction, mapped_reaction_smiles=mapped_reaction_smiles)

    def _map_reaction_smiles_batch(
        self, reaction_smiles_list: Sequence[str]
    ) -> list[str]:
        """Map a batch of reaction SMILES using the BatchedMapper.

        :param reaction_smiles_list: List of reaction SMILES strings to map.
        :type reaction_smiles_list: Sequence[str]

        :raises MapperError: If mapping fails for any reaction or
            RXNMapper returns >> placeholder.

        :return: List of atom-mapped reaction SMILES strings.
        :rtype: Sequence[str]
        """
        try:
            mapped_smiles_list = list(self._mapper.map_reactions(reaction_smiles_list))
        except Exception:
            # Some internal rxnmapper error occurred
            return [">>" for _ in reaction_smiles_list]

        return mapped_smiles_list

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Map a batch of reactions using the BatchedMapper.

        Dummy reactions (sentinels) are passed together with the valid reactions.
        If reaction was mapped successfully, it is replaced with a new Reaction object
        with the mapped_reaction_smiles field populated.
        If reaction was not mapped successfully, it is replaced with a SENTINEL.

        :param reactions: Batch of reactions to map.
        :type reactions: Sequence[Reaction]

        :return: Batch of reactions with mapped_reaction_smiles populated.
        :rtype: Sequence[Reaction]
        """
        reaction_smiles_list = tuple(reaction.reaction_smiles for reaction in reactions)

        mapped_results = self._map_reaction_smiles_batch(reaction_smiles_list)

        return tuple[Reaction, ...](
            (
                SENTINEL
                if reaction.dummy or mapped == ">>"
                else replace(reaction, mapped_reaction_smiles=mapped)
            )
            for reaction, mapped in zip(reactions, mapped_results)
        )
