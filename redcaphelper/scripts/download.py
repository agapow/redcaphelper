#! /usr/bin/env python
"""
Downloadthe contents or schema of a REDCap database.
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
from redcaphelper import utils


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


def make_save_name (conn, SAVE_NAME_TMPL):
	return 'backup.csv'


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

def parse_clargs (clargs):
	import argparse
	aparser = argparse.ArgumentParser()

	aparser.add_argument ('-u', "--url",
		help='url for uploading to',
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

	aparser.add_argument ('-l', "--log",
		help='where to log backup actions',
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

	return args



def main (clargs):
	import sys

	# get arguments (source db and output file)
	args = parse_clargs (sys.argv[1:])

	# connect to db & download backup
	utils.progress_msg ('Connecting to %s' % args.url)
	conn = new_connection (args.url, args.token)

	if args.outfile is None:
		save_name = make_save_name (conn, SAVE_NAME_TMPL)
	else:
		save_name = args.outfile
	utils.progress_msg ('Downloading %s backup' % args.type)
	recs = download_backup (conn, btype=args.type)

	utils.progress_msg ('Saving backup as %s' % save_name)
	flds = conn.field_names if args.type == 'data' else SCHEMA_FLD_ORDER
	save_backup (recs, save_name, flds)

	utils.progress_msg ("Finished", True)



if __name__ == '__main__':
	main()


### END ###
