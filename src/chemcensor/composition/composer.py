import csv
import logging
from collections.abc import Iterable
from collections.abc import Sequence
from os import PathLike
from pathlib import Path

from ..basic import Reaction
from ..configs import CompositionConfig
from ..db import DBManager
from ..db.stamp import build_stamp
from ..db.stamp import validate_db_version
from ..extraction import ReactionCenterExtractor
from ..processing import Processor
from .records import apply_center
from .records import apply_reaction
from .records import run_distributivity_postprocessing

logger = logging.getLogger(__name__)


def parse_csv_bool(value: str | None) -> bool:
    """Parse a CSV cell as a boolean (``1``/``true``/``yes`` → True)."""
    return (value or "").strip().lower() in {"1", "true", "yes", "y", "t"}


class ReactionCenterDBComposer:
    """Composes reaction center database from reference data."""

    def __init__(
        self,
        processor: Processor,
        reaction_center_extractor: ReactionCenterExtractor,
        batch_size: int = CompositionConfig.default_batch_size,
        reaction_smiles_column: str = "cleaned_rxn",
        document_id_column: str = "document_id",
        *,
        is_virtual_column: str = "is_virtual",
        source_column: str = "source_id",
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
        :param is_virtual_column: Column with per-row virtual flag
            (``0``/``1``, ``true``/``false``, …).
        :type is_virtual_column: str
        :param source_column: Column copied into ``Reaction.source`` /
            ``reactions.source`` (e.g. ``source_id``).
        :type source_column: str
        """
        self._manager = DBManager()
        self._processor = processor
        self._extractor = reaction_center_extractor
        self._batch_size = batch_size
        self._reaction_smiles_column = reaction_smiles_column
        self._document_id_column = document_id_column
        self._is_virtual_column = is_virtual_column
        self._source_column = source_column

    def _read(self, reference_data_path: PathLike) -> Iterable[Reaction]:
        """Read reactions from a CSV and convert each row into a
        :class:`Reaction` object.

        :param reference_data_path: Path to the CSV file.
        :return: An iterable of :class:`Reaction` objects.
        """
        with Path(reference_data_path).open() as fh:
            reader = csv.DictReader(fh)
            fieldnames = set(reader.fieldnames or ())
            has_virtual = self._is_virtual_column in fieldnames
            has_source = self._source_column in fieldnames
            for row in reader:
                yield Reaction(
                    reaction_smiles=row[self._reaction_smiles_column],
                    document_id=row[self._document_id_column],
                    source=(
                        (row.get(self._source_column) or "").strip()
                        if has_source
                        else ""
                    ),
                    is_virtual=(
                        parse_csv_bool(row.get(self._is_virtual_column))
                        if has_virtual
                        else False
                    ),
                )

    def _add_centers(self, reactions: Sequence[Reaction]) -> None:
        """Insert or update reaction centers from processed reactions.

        For each reaction center, if it already exists in the database
        (within the same virtuality group), its FG-signature is OR-ed with
        the new one (other columns are left unchanged). Otherwise, a new
        entry is created, including ``is_multi_component`` and ``components``.

        :param reactions: Reactions whose centers should be stored.
        :type reactions: Sequence[Reaction]
        """
        for reaction in reactions:
            for rc in reaction.reaction_centers.values():
                apply_center(
                    self._manager,
                    reaction_center_smiles=rc.reaction_center_smiles,
                    fg_signature=rc.fg_signature,
                    is_multi_component=rc.is_reaction_center_composite,
                    components=list(rc.reaction_center_components),
                    reaction_canonical_smiles=reaction.canonical_smiles,
                    sear_signature=reaction.sear_signature,
                    is_virtual=reaction.is_virtual,
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
        ``CompositionConfig.distributivity_threshold`` reactions, update its
        aggregate ``fg_signature`` with the bitwise AND of the signatures of
        its simple ``components``, when those component rows exist (same
        virtuality group).
        """
        run_distributivity_postprocessing(self._manager)

    def _add_reactions(self, reactions: Sequence[Reaction]) -> None:
        """Add a reaction to the database.

        :param reactions: Reactions to add.
        :type reactions: Sequence[Reaction]
        """
        for reaction in reactions:
            apply_reaction(
                self._manager,
                reaction.canonical_smiles,
                reaction.document_id,
                is_virtual=reaction.is_virtual,
                source=reaction.source,
            )

    def compose(
        self,
        reference_data_path: PathLike,
        output_data_path: PathLike,
        *,
        db_version: str,
    ) -> None:
        """Compose reaction-center database from reference data.

        1. Stream reactions from the CSV file, collecting them into
           fixed-size batches.
        2. For each batch, run the processing pipeline, store reactions
           and reaction centers (excluding SIS reactions) in the database.
           Per-row ``is_virtual`` / ``source`` come from the CSV.
        3. Run post-processing (distributivity of FG bits for frequent
           multi-component centers).
        4. Write the build stamp and dump the in-memory database to
           *output_data_path*.

        :param reference_data_path: Path to the input CSV.
        :param output_data_path: Path where the SQLite database will be saved.
        :param db_version: Catalog version label for this build (e.g. ``U3-1``),
            stored inside the database so consumers can identify the build.
        :raises InvalidDBVersionError: If *db_version* is empty or blank.
        """
        # Validated up front so a missing label fails before the expensive
        # composition loop rather than after it. The stamp itself is built
        # just before it is written so ``built_at`` reflects when the file was
        # written, not when composition started.
        validate_db_version(db_version)

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
        stamp = build_stamp(db_version)
        self._manager.write_metadata(stamp)
        self._manager.dump(output_data_path)
        logger.info(
            f"Database saved to {output_data_path} "
            f"(db_version={stamp['db_version']})"
        )
