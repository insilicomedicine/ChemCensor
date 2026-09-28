import argparse
import logging
from pathlib import Path

from chemcensor.db.manager import DBManager
from chemcensor.db.stamp import stamp_database_file

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-path",
        type=Path,
        required=True,
        help="Path to the SQLite database to stamp, modified in place.",
    )
    parser.add_argument(
        "--db-version",
        required=True,
        help="Catalog version label to record (e.g. U3-1).",
    )
    parser.add_argument(
        "--built-at",
        default=None,
        help=(
            "Build timestamp as an ISO-8601 UTC string "
            "(e.g. 2026-08-20T09:14:02Z). Defaults to now."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing, different db_version.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    args = parse_args()

    existing = DBManager.read_metadata(args.db_path)
    if existing:
        logger.info("Existing stamp: %s", existing)
    else:
        logger.info("Database carries no stamp yet.")

    stamp = stamp_database_file(
        args.db_path,
        args.db_version,
        built_at=args.built_at,
        force=args.force,
    )
    logger.info("Wrote stamp to %s: %s", args.db_path, stamp)


if __name__ == "__main__":
    main()
