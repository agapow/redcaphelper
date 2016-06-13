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

import os
from redcaphelper import utils, csvutils, connection
from redcaphelper import __version__ as version


### MAIN

def parse_clargs (clargs):
	import argparse
	aparser = argparse.ArgumentParser (
		description='download contents or schema of a REDCap database'
	)

	#TODO: KJ - need to add other clargs here; check the connection object

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

	#TODO: KJ - Need to do some error handling of input etc
	utils.msg_progress ('Uploading records')
	recs = csvutils.read_csv(args.infile)
	conn.import_recs(recs)

	utils.msg_progress ("Finished", True)



if __name__ == '__main__':
	main()


### END ###
