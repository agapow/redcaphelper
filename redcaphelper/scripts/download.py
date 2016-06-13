#! /usr/bin/env python
"""
Download the contents or schema of a REDCap database.
"""

### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import range

import csv
import os
import io

import redcap
from redcaphelper import utils, csvutils, connection, constants
from redcaphelper import __version__ as version


### CONSTANTS & DEFINES

SAVE_NAME_TMPL = 'foo.csv'

SCHEMA_FLD_ORDER = [
	'field_name',
	'form_name',
	'section_header',
	'field_type',
	'field_label',
	'select_choices_or_calculations',
	'field_note',
	'text_validation_type_or_show_slider_number',
	'text_validation_min',
	'text_validation_max',
	'identifier',
	'branching_logic',
	'required_field',
	'custom_alignment',
	'question_number',
	'matrix_group_name',
	'matrix_ranking',
]


### CODE ###

def new_connection (url, token):
	return redcap.Project (url, token)


def download_backup (conn, btype='data'):
	if btype == 'schema':
		csv_txt = conn.export_metadata (format='csv')
		csv_rdr = csv.DictReader (io.StringIO (csv_txt))
		csv_recs = [r for r in csv_rdr]
	elif btype == 'data':
		csv_recs = chunked_export (conn)
	else:
		raise ValueError ("unknown backup type '%s'" % btype)
	return csv_recs


def save_backup (recs, pth, flds):
	utils.write_csv (recs, pth, flds)


### MAIN

def parse_clargs ():
	import argparse
	aparser = argparse.ArgumentParser()

	aparser.add_argument ('-u', "--url",
		help='url for download',
		default=None,
	)

	aparser.add_argument ('-t', "--token",
		help='API token',
		default=None,
	)

	aparser.add_argument ('-o', "--outfile",
		help='where the backup is to be saved',
		default=None,
	)

	aparser.add_argument ('-y', "--type",
		help='download schema or data',
		choices=['data', 'schema'],
		default='data',
	)

	args = aparser.parse_args()

	if args.url is None:
		args.url = os.environ['REDCAP_API_URL']
	if args.token is None:
		args.token= os.environ['REDCAP_API_TOKEN']
	if args.outfile is None:
		if args.type is 'data':
			args.outfile = 'args.data.csv'
		else:
			args.outfile = 'args.schema.csv'

	return args



def main (clargs):
	# get arguments (source db and output file)
	args = parse_clargs()

	# connect to db & download backup
	utils.progress_msg ('Connecting to %s' % args.url)
	conn = new_connection (args.url, args.token)

	utils.progress_msg ('Downloading %s backup' % args.type)
	recs = download_backup (conn, btype=args.type)

	utils.progress_msg ('Saving backup as %s' % save_name)
	flds = conn.field_names if args.type == 'data' else SCHEMA_FLD_ORDER
	save_backup (recs, args.outfile, flds)

	utils.progress_msg ("Finished", True)



if __name__ == '__main__':
	main()


### END ###
