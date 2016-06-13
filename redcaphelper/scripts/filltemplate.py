"""
Given a set of CSV records and the import template for a REDCap database,
format the records appropriately.
"""

### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()

import pandas
import csvutils

from redcaphelper import __version__ as version


### CONSTANTS & DEFINES

### CODE ###

def fill_template (records, template):
	"""
	Uses pandas update method to fill in a template empty data frame with the data in records, while
	retaining only the template columns. Extra columns in records but not in the template will be lost;
	columns in template but not in the passed record will be filled with blanks (NaN).
	"""
	fill_tmpl = pandas.DataFrame (template)
	fill_tmpl = fill_tmpl.reindex (records.index)
	fill_tmpl.update (records)
	return fill_tmpl


### MAIN

def parse_clargs (clargs):
	import argparse
	aparser = argparse.ArgumentParser (
		description='fill in a REDCap db import template from a list of records'
	)

	aparser.add_argument('--version', action='version', version='%s' % version)

	aparser.add_argument ("csvfile", help='CSV file to be imported to template')

	aparser.add_argument ("template", help='a REDCap import template')

	aparser.add_argument('-o', '--outfile',
		default='filled-template.csv',
		help='file to output to',
	)

	args = aparser.parse_args()

	return args


def main(clargs):
	args = parse_clargs()

	with open(args.csvfile, 'r') as in_hndl:
		records = pandas.read_csv (in_hndl, index_col = 0)

	with open(args.template, 'r') as in_hndl2:
		template = pandas.read_csv (in_hndl2, index_col = 0)

	filledtemplate = fill_template (records, template)

	with open (args.outfile, 'w') as out_hndl:
		filledtemplate.to_csv (out_hndl, na_rep=None)
if __name__ == '__main__':
	main()



### END ###
