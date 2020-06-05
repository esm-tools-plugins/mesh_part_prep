#!/usr/bin/env python3
"""A preprocessort for the mesh partitioner"""

__author__ = "Paul Gierz"
__email__ = "pgierz@awi.de"
__version__ = "1.0.0"

import logging

from .mesh_part_prep import *

# Create the logger:
logger = logging.getLogger("mesh_part_prep")
# Create a console handler:
ch = logging.StreamHandler()

# create formatter and add it to the handlers:
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
