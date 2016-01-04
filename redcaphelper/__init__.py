"""
Utilities & scripts for working with REDCap web databases.

When working with a REDCap database, several regular tasks can become tedious -
uploading a large dataset in parts, backing up the data & schema, extracting
the latest import template. The package provides code fto help with these
routine tasks, allowing them to be easily scripted and automated. It heavily
leverages the PyCap package.
"""

__version__ = '0.1'

### IMPORTS

from connection import *


### END ###
