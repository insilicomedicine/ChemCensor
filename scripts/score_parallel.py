from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

from chemcensor.parallel import ParallelConfig
from chemcensor.parallel import score_file


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Route stdlib loggers to stderr and an optional file.

    Mirrors :func:`scripts.compose_database.configure_logging`: set
    ``CHEMCENSOR_LOG_FILE`` to additionally append all messages to a
    file (useful for long unattended runs).
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
    logging.getLogger("transformers").setLevel(logging.WARNING)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score a CSV library of reactions in parallel.",
    )
    parser.add_argument("input_csv", type=Path, help="Input CSV path.")
    parser.add_argument("output_csv", type=Path, help="Output CSV path.")
    parser.add_argument(
        "--db",
        dest="db_path",
        type=Path,
        required=True,
        help="Path to the SQLite reaction-centers database.",
    )
    parser.add_argument(
        "--smiles-column",
        default="reaction_smiles",
        help="CSV column with reaction SMILES (default: %(default)s). "
        "With --fake-mapper this column must hold precomputed atom-mapped "
        "reaction SMILES.",
    )
    parser.add_argument(
        "--fake-mapper",
        action="store_true",
        help="Reuse precomputed atom maps from --smiles-column via FakeMapper "
        "instead of running rxnmapper (no GPU; disables the length check).",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=None,
        help="Optional .ckpt path for resumable runs.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of scorer worker processes. Default: auto.",
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
        help="SMILES per scoring batch (default: %(default)s).",
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
        "--no-exact-match",
        action="store_true",
        help="Skip the exact-match canonical SMILES lookup.",
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
        help="Recycle scorer workers after this many batches. Default: never.",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=1000,
        help="Reactions between checkpoint flushes (default: %(default)s).",
    )
    return parser.parse_args()


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
        find_exact_match=not args.no_exact_match,
        progress=not args.no_progress,
        maxtasksperchild=args.maxtasksperchild,
        checkpoint_interval=args.checkpoint_interval,
        use_fake_mapper=args.fake_mapper,
    )
    logger.info(
        "Starting parallel scoring: input=%s output=%s db=%s config=%s",
        args.input_csv,
        args.output_csv,
        args.db_path,
        config,
    )
    started = time.time()
    score_file(
        input_path=args.input_csv,
        output_path=args.output_csv,
        db_path=args.db_path,
        smiles_column=args.smiles_column,
        config=config,
        checkpoint_path=args.checkpoint,
    )
    logger.info("Done in %.2fs", time.time() - started)


if __name__ == "__main__":
    main()
