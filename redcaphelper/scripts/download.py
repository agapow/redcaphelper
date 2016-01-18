#! /usr/bin/env python
"""
Downloadthe contents or schema of a REDCap database.
"""

### IMPORTS

import os
from redcaphelper import utils, csvutils, connection, constants

### MAIN

def parse_clargs (clargs):
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
		default='redcap.out.csv',
	)

	#TODO: KJ - Not sure what's being done with these logs; to check & finish later
	#aparser.add_argument ('-l', "--log",
	#	help='where to log backup actions',
	#	default=None,
	#)

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
	utils.msg_progress ('Connecting to %s' % args.url)
	conn = Connection (args.url, args.token)
	
	#???: KJ -Single script for downloading both schema and records (as now), or better to have one for each?
	utils.msg_progress ('Downloading %s backup' % args.type)
	recs = conn.export_recs() if args.type == 'data' else conn.export_schema()
	
	utils.progress_msg ('Saving backup as %s' % args.outfile)
	flds = conn.export_field_names() if args.type == 'data' else constants.SCHEMA_FLD_ORDER
	csvutils.write_csv (recs, args.outfile, hdr_flds=flds)
	
	utils.msg_progress ("Finished", True)
 
	

if __name__ == '__main__':
	main()


### END ###