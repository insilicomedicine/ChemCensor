from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

from chemcensor.parallel import compose_file
from chemcensor.parallel import ParallelConfig


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Route stdlib loggers (rxnmapper, etc.) to stderr and an optional file.

    Mirrors :func:`scripts.compose_database.configure_logging` and
    :func:`scripts.score_parallel.configure_logging`: set
    ``CHEMCENSOR_LOG_FILE`` to additionally append all messages to a file
    (useful for long unattended runs / diagnosing memory issues).
    """
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    log_path = os.environ.get("CHEMCENSOR_LOG_FILE")
    if log_path:
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    for handler in handlers:
        handler.setFormatter(fmt)
    logging.basicConfig(level=logging.INFO, handlers=handlers, force=True)
    logging.getLogger("rxnmapper").setLevel(logging.DEBUG)
    logging.getLogger("transformers").setLevel(logging.WARNING)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose a reaction-center SQLite database from a reference "
        "CSV, in parallel. Expected columns include cleaned_rxn, PatentNumber, "
        "and optionally is_virtual and source_id."
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to the input CSV.",
    )
    parser.add_argument(
        "output_sqlite",
        type=Path,
        help="Path for the output SQLite database file.",
    )
    parser.add_argument(
        "--db-version",
        required=True,
        help=(
            "Catalog version label for this build (e.g. U3-1). Stored inside the "
            "database so consumers can identify which build they are using."
        ),
    )

    parser.add_argument(
        "--reaction-smiles-column",
        default="cleaned_rxn",
        help="CSV column name for reaction SMILES (default: %(default)s). "
        "With --fake-mapper this column must hold precomputed atom-mapped "
        "reaction SMILES.",
    )
    parser.add_argument(
        "--document-id-column",
        default="PatentNumber",
        help="CSV column name for document ID (default: %(default)s).",
    )
    parser.add_argument(
        "--is-virtual-column",
        default="is_virtual",
        help="CSV column for the per-row virtual flag (default: %(default)s). "
        "If absent, all rows are treated as real.",
    )
    parser.add_argument(
        "--source-column",
        default="source_id",
        help="CSV column copied into reactions.source (default: %(default)s). "
        "If absent, source is left empty.",
    )
    parser.add_argument(
        "--fake-mapper",
        action="store_true",
        help="Reuse precomputed atom maps from --reaction-smiles-column via "
        "FakeMapper instead of running rxnmapper (no GPU; disables the length "
        "check).",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Run rxnmapper on CPU instead of GPU.",
    )
    parser.add_argument(
        "--save-mapped",
        action="store_true",
        help="After a successful run, write the atom maps computed by rxnmapper "
        "back into the input CSV as --mapped-column (all other columns are "
        "preserved), so a later run over the same CSV can pass --fake-mapper "
        "--reaction-smiles-column <mapped column> and skip rxnmapper. Cannot be "
        "combined with --fake-mapper.",
    )
    parser.add_argument(
        "--save-mapped-to",
        type=Path,
        default=None,
        help="Write the CSV with the atom-mapped column to this path instead of "
        "updating the input CSV in place. Implies --save-mapped.",
    )
    parser.add_argument(
        "--mapped-column",
        default="mapped_rxn",
        help="Column holding the saved atom-mapped SMILES (default: %(default)s).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of composer worker processes. Default: auto.",
    )
    parser.add_argument(
        "--mappers",
        type=int,
        default=None,
        help="Number of rxnmapper (mapper) processes. Default: auto.",
    )
    parser.add_argument(
        "--mapper-threads",
        type=int,
        default=None,
        help="OMP threads per mapper subprocess. Default: auto (1).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="SMILES per processing batch (default: %(default)s).",
    )
    parser.add_argument(
        "--mapper-batch-size",
        type=int,
        default=32,
        help="Internal rxnmapper batch size (default: %(default)s).",
    )
    parser.add_argument(
        "--max-center-type",
        type=int,
        default=4,
        choices=[1, 2, 3, 4],
        help="Maximum reaction center type to extract (default: %(default)s).",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the tqdm progress bar.",
    )
    parser.add_argument(
        "--maxtasksperchild",
        type=int,
        default=None,
        help="Recycle composer workers after this many batches. Default: never.",
    )
    args = parser.parse_args()
    if (args.save_mapped or args.save_mapped_to is not None) and args.fake_mapper:
        parser.error(
            "--save-mapped is pointless with --fake-mapper: the atom maps are "
            "already in the input CSV"
        )
    return args


def main() -> None:
    configure_logging()
    args = parse_args()

    config = ParallelConfig(
        n_workers=args.workers,
        n_mappers=args.mappers,
        mapper_threads=args.mapper_threads,
        batch_size=args.batch_size,
        mapper_internal_batch_size=args.mapper_batch_size,
        max_center_type=args.max_center_type,
        progress=not args.no_progress,
        maxtasksperchild=args.maxtasksperchild,
        use_fake_mapper=args.fake_mapper,
        use_cpu=args.cpu,
    )
    save_mapped_path: Path | None = args.save_mapped_to
    if save_mapped_path is None and args.save_mapped:
        save_mapped_path = args.input_csv

    logger.info(
        "Starting parallel composition: input=%s output=%s db_version=%s config=%s",
        args.input_csv,
        args.output_sqlite,
        args.db_version,
        config,
    )
    started = time.time()
    compose_file(
        input_path=args.input_csv,
        output_path=args.output_sqlite,
        db_version=args.db_version,
        reaction_smiles_column=args.reaction_smiles_column,
        document_id_column=args.document_id_column,
        config=config,
        is_virtual_column=args.is_virtual_column,
        source_column=args.source_column,
        save_mapped_path=save_mapped_path,
        mapped_column=args.mapped_column,
    )
    logger.info("All done. Time spent: %.2f seconds", time.time() - started)


if __name__ == "__main__":
    main()
