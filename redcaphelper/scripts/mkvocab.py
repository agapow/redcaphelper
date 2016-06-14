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
import argparse

from redcaphelper import __version__ as version


### CONSTANTS & DEFINES

SPACE_PATT = re.compile ('[]\s\.\,\-\:\/\\\(\)]+')
SPACE_PATT = re.compile ('[^0-9a-zA-Z]+')


### CODE ###

def make_vc_value (vc_label):
	# lower
	val_str = vc_label.lower()
	# replace possessives
	val_str = val_str.replace ("'s'", 's')
	# non-alphanumerics become whitespace
	val_str = SPACE_PATT.sub (' ', val_str)
	# strip flanking whitespace
	val_str = val_str.strip()
	# internal whitespace becomes single underscore
	val_str = val_str.replace (' ', '_')
	return val_str


def lines_to_vocab (lines, as_lines):
	if as_lines:
		sep = '\n'
	else:
		sep = ' | '
	return sep.join (["%s, %s" % (make_vc_value (l), l) for l in lines])


### MAIN

def parse_clargs():
	parser = argparse.ArgumentParser (description='produce REDCap vocabularies for fields with choices')

	parser.add_argument ('--version', action='version',
		version='%s' % version)
	parser.add_argument ('-a', '--as-lines', action='store_true',
		help='produce output with an item per line')
	parser.add_argument ('infiles', nargs='*')

	return parser.parse_args()


def main():
	args = parse_clargs()

	# if file, read file
	if args.infiles:
		for a in args.infiles:
			with open (args[0], 'rU') as in_hndl:
				lines = [l.strip() for l in in_hndl.readlines() if l.strip()]
				print (lines_to_vocab (lines, args.as_lines))
	else:
		lines = [l.strip() for l in sys.stdin if l.strip()]
		print (lines_to_vocab (lines, args.as_lines))



if __name__ == '__main__':
	main()


### END ###
