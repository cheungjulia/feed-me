"""Lightweight logger module."""

import logging
import sys

# Create logger
logger = logging.getLogger("nommer")
logger.setLevel(logging.INFO)

# Console handler with simple format
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

