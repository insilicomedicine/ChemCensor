import csv
import logging
from collections.abc import Iterable
from collections.abc import Sequence
from os import PathLike
from pathlib import Path

import numpy as np

from ..basic import Reaction
from ..configs import CompositionConfig
from ..db import DBManager
from ..extraction import ReactionCenterExtractor
from ..processing import Processor

logger = logging.getLogger(__name__)


class ReactionCenterDBComposer:
    """Composes reaction center database from reference data."""

    def __init__(
        self,
        processor: Processor,
        reaction_center_extractor: ReactionCenterExtractor,
        batch_size: int = CompositionConfig.default_batch_size,
        reaction_smiles_column: str = "reaction_smiles",
        document_id_column: str = "document_id",
    ) -> None:
        """Initialize composer with required components.

        :param processor: Reaction processor (e.g. ReactionProcessor).
        :type processor: Processor
        :param reaction_center_extractor: Extractor for reaction centers and
            functional-group signatures.
        :type reaction_center_extractor: ReactionCenterExtractor
        :param batch_size: Fixed number of reactions per processing batch.
        :type batch_size: int
        :param reaction_smiles_column: Column name in the CSV file that contains
            the reaction SMILES.
        :type reaction_smiles_column: str
        :param document_id_column: Column name in the CSV file that contains
            the document ID.
        :type document_id_column: str
        """
        self._manager = DBManager()
        self._processor = processor
        self._extractor = reaction_center_extractor
        self._batch_size = batch_size
        self._reaction_smiles_column = reaction_smiles_column
        self._document_id_column = document_id_column

    def _read(self, reference_data_path: PathLike) -> Iterable[Reaction]:
        """Read reactions from a CSV file containing a ``reaction_smiles``
        column and convert each row into a :class:`Reaction` object.

        :param reference_data_path: Path to the CSV file.
        :return: An iterable of :class:`Reaction` objects.
        """
        with Path(reference_data_path).open() as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                yield Reaction(
                    reaction_smiles=row[self._reaction_smiles_column],
                    document_id=row[self._document_id_column],
                )

    def _add_centers(self, reactions: Sequence[Reaction]) -> None:
        """Insert or update reaction centers from processed reactions.

        For each reaction center, if it already exists in the database,
        its FG-signature is OR-ed with the new one (other columns are left
        unchanged). Otherwise, a new entry is created, including
        ``is_multi_component`` and ``components``.

        :param reactions: Reactions whose centers should be stored.
        :type reactions: Sequence[Reaction]
        """
        for reaction in reactions:
            for rc in reaction.reaction_centers.values():
                existing = self._manager.find_center(rc.reaction_center_smiles)
                if existing is not None:
                    combined = np.bitwise_or(existing, rc.fg_signature)
                    self._manager.update(rc.reaction_center_smiles, combined)
                else:
                    self._manager.add_reaction_center(
                        rc.reaction_center_smiles,
                        rc.fg_signature,
                        is_multi_component=rc.is_reaction_center_composite,
                        components=list(rc.reaction_center_components),
                    )
                if not self._manager.find_center_to_reaction(
                    rc.reaction_center_smiles, reaction.canonical_smiles
                ):
                    self._manager.add_center_to_reaction(
                        rc.reaction_center_smiles,
                        reaction.canonical_smiles,
                        rc.fg_signature,
                        reaction.sear_signature,
                    )

    def _compose_batch(self, batch: Sequence[Reaction]) -> None:
        """Process a single batch: run the processing pipeline, insert
        reactions, filter out SIS reactions, extract and store centers.

        :param batch: Batch of raw reactions to process.
        :type batch: Sequence[Reaction]
        """
        processed = self._processor.process_batch(batch)

        self._add_reactions(processed)

        non_sis = tuple(r for r in processed if not r.is_sis_reaction)
        extracted = self._extractor.extract_rc_for_batch(non_sis)
        self._add_centers(extracted)

    def _run_postprocessing(self) -> None:
        """Apply FG-signature distributivity for frequent multi-component centers.

        For each multi-component center that appears in more than
        ``CompositionConfig.distributivity_threshold`` reactions, update its aggregate
        ``fg_signature`` with the bitwise AND of the signatures of its simple
        ``components``, when those component rows exist.
        """
        for (
            center_smiles,
            current_fg_sig,
            components,
        ) in self._manager.list_multi_component_for_dist(
            CompositionConfig.distributivity_threshold
        ):
            comp_sigs = [
                self._manager.find_center(comp_smiles)
                for comp_smiles in set(components)
            ]
            comp_sigs_no_none = [x for x in comp_sigs if x is not None]
            if comp_sigs_no_none:
                combined = np.bitwise_and.reduce(comp_sigs_no_none)
                merged = np.bitwise_or(current_fg_sig, combined)
                self._manager.update(center_smiles, merged)

    def _add_reactions(self, reactions: Sequence[Reaction]) -> None:
        """Add a reaction to the database.

        :param reactions: Reactions to add.
        :type reactions: Sequence[Reaction]
        """
        for reaction in reactions:
            document_id = self._manager.find_reaction(reaction.canonical_smiles)
            if document_id is not None and reaction.document_id in document_id:
                continue
            self._manager.add_reaction(reaction.canonical_smiles, reaction.document_id)

    def compose(
        self, reference_data_path: PathLike, output_data_path: PathLike
    ) -> None:
        """Compose reaction-center database from reference data.

        1. Stream reactions from the CSV file, collecting them into
           fixed-size batches.
        2. For each batch, run the processing pipeline, store reactions
           and reaction centers (excluding SIS reactions) in the database.
        3. Run post-processing (distributivity of FG bits for frequent
           multi-component centers).
        4. Dump the in-memory database to *output_data_path*.

        :param reference_data_path: Path to the input CSV.
        :param output_data_path: Path where the SQLite database will be saved.
        """
        batch: list[Reaction] = []
        batch_count = 0
        for reaction in self._read(reference_data_path):
            batch.append(reaction)
            if len(batch) >= self._batch_size:
                self._compose_batch(batch)
                batch_count += 1
                batch = []
        if batch:
            self._compose_batch(batch)
            batch_count += 1

        logger.info(f"Processed {batch_count} batches of size {self._batch_size}")
        self._run_postprocessing()
        self._manager.dump(output_data_path)
        logger.info(f"Database saved to {output_data_path}")
