#! /usr/bin/env python
"""
Downloadthe contents or schema of a REDCap database.
"""

### IMPORTS

import os
from redcaphelper import utils, csvutils, connection

### MAIN

def parse_clargs (clargs):
	import argparse
	aparser = argparse.ArgumentParser()

	aparser.add_argument ('-u', "--url",
		help='url for upload',
		default=None,
	)

	aparser.add_argument ('-t', "--token",
		help='API token',
		default=None,
	)

	aparser.add_argument ("infile",
		help='file to be imported to redcap'
	)

	)

	args = aparser.parse_args()

	if args.url is None:
		args.url = os.environ['REDCAP_API_URL']
	if args.token is None:
		args.token= os.environ['REDCAP_API_TOKEN']
	
	return args
		
			
	
def main (clargs):
	import sys
	args = parse_clargs (sys.argv[1:])

	#Connect to database
	utils.msg_progress ('Connecting to %s' % args.url)
	conn = Connection (args.url, args.token)
	
	#TODO: KJ - Need code for uploading to database here; need to do some error handling of input etc
	utils.msg_progress ('Uploading records')
	recs = csvutils.read_csv(args.infile)
	conn.import_recs(recs)
	
	utils.msg_progress ("Finished", True)
 
	

if __name__ == '__main__':
	main()


### END ###