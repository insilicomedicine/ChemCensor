import os
from dataclasses import replace
from typing import Any
from typing import Sequence

from ..basic import Reaction
from ..basic import SENTINEL
from .errors.mapper_errors import JobSpecificationError
from .errors.mapper_errors import MapperError


def _create_batched_mapper(batch_size: int, *, use_cpu: bool) -> Any:
    """Create rxnmapper with CUDA hidden temporarily when CPU mode is requested.

    The import is deliberately lazy: importing rxnmapper loads torch and may
    probe CUDA, so ``CUDA_VISIBLE_DEVICES`` must be set before that import.
    Restoring the variable after construction prevents CPU mode from leaking
    into unrelated code in the caller process; the created model remains on
    the device selected during construction.

    :param batch_size: Batch size for rxnmapper inference.
    :type batch_size: int
    :param use_cpu: Whether to hide CUDA while importing and constructing
        rxnmapper.
    :type use_cpu: bool
    :return: Configured ``rxnmapper.BatchedMapper`` instance.
    :rtype: Any
    """
    previous_cuda_devices = os.environ.get("CUDA_VISIBLE_DEVICES")
    if use_cpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        from rxnmapper import BatchedMapper

        return BatchedMapper(canonicalize=True, batch_size=batch_size)
    finally:
        if use_cpu:
            if previous_cuda_devices is None:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            else:
                os.environ["CUDA_VISIBLE_DEVICES"] = previous_cuda_devices


class Mapper:
    """Mapper implementation for reaction mapping."""

    def __init__(
        self, batch_size: int = 1, n_jobs: int = 1, *, use_cpu: bool = False
    ) -> None:
        """Initialize Mapper.

        :param batch_size: Batch size for mapping.
        :type batch_size: int
        :param n_jobs: Number of jobs for mapping. Used as the
            ``OMP_NUM_THREADS`` default when the process does not already
            define that variable. An existing process-wide setting is
            preserved.
        :type n_jobs: int
        :param use_cpu: When ``True``, hide CUDA before lazily importing and
            constructing ``BatchedMapper`` so rxnmapper runs on CPU. The
            previous ``CUDA_VISIBLE_DEVICES`` value is restored afterwards.
            CPU-mode construction is not thread-safe because this temporarily
            changes the process environment; construct mappers before starting
            application worker threads.
        :type use_cpu: bool
        """
        if n_jobs < 1:
            raise JobSpecificationError(msg="n_jobs must be greater than 0")

        self.use_cpu = use_cpu
        os.environ.setdefault("OMP_NUM_THREADS", str(n_jobs))
        self._mapper = _create_batched_mapper(batch_size, use_cpu=use_cpu)

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
            mapped_smiles_list = []
        else:
            if len(mapped_smiles_list) == len(reaction_smiles_list):
                return mapped_smiles_list
            mapped_smiles_list = []
        for reaction_smiles in reaction_smiles_list:
            try:
                mapped_smiles_list.append(
                    next(self._mapper.map_reactions([reaction_smiles]))
                )
            except Exception:
                mapped_smiles_list.append(">>")
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
