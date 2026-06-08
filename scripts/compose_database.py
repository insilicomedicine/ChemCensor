import argparse
import logging
import os
import sys
import time
from pathlib import Path

from chemcensor.basic import ReactionCenterType
from chemcensor.composition import ReactionCenterDBComposer
from chemcensor.extraction import ReactionCenterExtractor
from chemcensor.processing import BatchFilter
from chemcensor.processing import CanoRxnAnnotator
from chemcensor.processing import Mapper
from chemcensor.processing import OrphanRemover
from chemcensor.processing import ReactionProcessor
from chemcensor.processing import SeArAnnotator
from chemcensor.processing import SisAnnotator
from chemcensor.processing import StaticStereoValidator
from chemcensor.processing import TransformCreator
from chemcensor.processing import Validator
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR

logger = logging.getLogger(__name__)

_BATCH_SIZE = 32
# Disclaimer: BATCH_SIZE is supposed to be as low as possible to avoid memory issues
# Moreover, the higher the batch size, the greater the chance of one thread processing
# since every error in the batch will switch to sequntial processing. The recommended
# batch size is 32 or 16.


def configure_logging() -> None:
    """Route stdlib loggers (rxnmapper, etc.) to stderr and optional file.

    Rxnmapper attaches NullHandler to its loggers; without this, chunk fallback
    warnings never appear. Set CHEMCENSOR_LOG_FILE=/path/to.log for a dedicated file.
    In case of memory issues, they will be written to the file.
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

    # Chunk-level fallback: WARNING; per-reaction errors in fallback: INFO
    logging.getLogger("rxnmapper").setLevel(logging.DEBUG)
    logging.getLogger("transformers").setLevel(logging.WARNING)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose a reaction-center SQLite database from a reference CSV."
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to the input CSV (reaction SMILES + document id columns).",
    )
    parser.add_argument(
        "output_sqlite",
        type=Path,
        help="Path for the output SQLite database file.",
    )
    parser.add_argument(
        "--reaction-smiles-column",
        default="cleaned_rxn",
        help="CSV column name for reaction SMILES (default: %(default)s).",
    )
    parser.add_argument(
        "--document-id-column",
        default="PatentNumber",
        help="CSV column name for document ID (default: %(default)s).",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    start_time = time.time()

    processor = ReactionProcessor(
        (
            Validator(),
            Mapper(batch_size=_BATCH_SIZE),
            OrphanRemover(),
            TransformCreator(),
            CanoRxnAnnotator(),
            SisAnnotator(),
            StaticStereoValidator(),
            SeArAnnotator(FG_COLLECTION_SEAR),
            BatchFilter(),
        )
    )
    extractor = ReactionCenterExtractor(max_center_type=ReactionCenterType.RC4)

    composer = ReactionCenterDBComposer(
        processor=processor,
        reaction_center_extractor=extractor,
        batch_size=_BATCH_SIZE,
        reaction_smiles_column=args.reaction_smiles_column,
        document_id_column=args.document_id_column,
    )

    composer.compose(args.input_csv, args.output_sqlite)

    elapsed = time.time() - start_time
    logger.info(f"All done. Time spent: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
