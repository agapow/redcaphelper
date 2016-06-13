#!/usr/bin/env python

"""
Read input and transform lines into a vocabulary suitable for REDCap.
"""

### IMPORTS

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import sys

import re

from redcaphelper import __version__ as version


### CONSTANTS & DEFINES

SPACE_PATT = re.compile ('[]\s\.\,\-\:\/\\\(\)]+')


### CODE ###

def make_vc_value (vc_label):
	val_str = vc_label.lower().strip()
	val_str = SPACE_PATT.sub ('_', val_str)
	return val_str


### MAIN

def main (clargs):
	import sys
	args = parse_clargs (sys.argv[1:])
	assert len (args) <= 2, "can only accept one file on the commandline"

	# if file, read file
	if args:
		with open (args[0], 'rU') as in_hndl:
			lines = [l.strip() for l in in_hndl.readlines()]
	else:
		lines = [l.strip() for l in sys.stdin]

	# parse and print line
	print (' | '.join (["%s, %s" % (make_vc_value (l), l) for l in lines]))


if __name__ == '__main__':
	main()


### END ###
