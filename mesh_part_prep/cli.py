#!/usr/bin/env python

import argparse
import logging
import sys


logging.basicConfig(level=logging.DEBUG)

def parse_args():
    """
    Parsers command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mesh_dir", help="Path to the unpartioned mesh directory", default=None)
    return parser.parse_args()

def main():
    args = parse_args()
    logging.debug(args)
    sys.exit(0)

if __name__ == "__main__":
    main()
