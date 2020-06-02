#!/usr/bin/env python

import argparse
import logging
import sys

import mesh_part_prep  # PG: Relative import??


def parse_args():
    """
    Parsers command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mesh_dir", help="Path to the unpartioned mesh directory", default=None
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="logLevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    logger = logging.getLogger("mesh_part_prep")
    if args.logLevel:
        logger.setLevel(level=getattr(logging, args.logLevel))
    logger.debug(args)

    rm = mesh_part_prep.RawMesh(path=args.mesh_dir)
    rm.process()

    sys.exit(0)


if __name__ == "__main__":
    main()
