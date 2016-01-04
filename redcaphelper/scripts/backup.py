#!/Users/pagapow/anaconda/bin/python
"""
Read a list of REDCap backups and run them all.

Does not do the actual backups, this is handled by another script. This script
is deliberately inflexible (e.g. no commandline args) as it is meant to be
called by cron, not used as a standalone general script. It is configured via
all the settings at the top.
"""

from __future__ import print_function
from builtins import str

__version__ = 0.3

# TODO: logging?
# TODO: read config file
# TODO: encrypt


### IMPORTS

import logging
import datetime
import os

import yaml



### CONSTANTS & DEFINES

# execution parameters
PYTHON_EXE = '/Users/pagapow/anaconda/bin/python'
BACKUP_SCRIPT = '~/Documents/Projects/Imperial/Projects/Euclids\ cyberinfrastructure/Scripts/Convert\ inform\ to\ REDCap/backup-redcap-db.py'
BACKUP_PARAMS = 'redcap-backup.yaml'
SAVEAS = '${name}-${type}-${datetime}.redcap-backup'
BACKUP_CLI = '{exe} {script} {type} {log} {saveas} {url} {token}'
DATETIME_FMT = '%Y%m%dT%H%M%S'
BCRYPT_EXE = '/usr/local/bin/bcrypt'

# unused
LOG = 'redcap-backup.log'


### CODE ###

def safe_format (s, mapping):
	import string
	t = string.Template (s)
	return t.safe_substitute (mapping)


def datetime_str ():
	dt = datetime.datetime.now()
	return dt.strftime (DATETIME_FMT)


def progress_msg (m):
	print (m)


def read_db_list (pth):
	# TODO: assert that config file exists
	with open (pth, 'rU') as in_hndl:
		data = yaml.load (in_hndl)
	backup_params = data.get ('backup', None)
	assert backup_params, 'configuration file does not have backup section'
	return backup_params


def run_one_backup (s, encrypt, log, saveas):
	## Preconditions:
	assert 'name' in s, 'source missing name'
	assert 'url' in s, 'source %s missing name' % s['name']
	assert 'token' in s, 'source %s missing name' %  s['name']

	## Main:
	progress_msg ('Backing up %s ...' % s['name'])

	for t in ['data', 'schema']:
	# build the save path name
		savepath = safe_format (saveas, {
				'name': s['name'],
				'type': t,
				'datetime': datetime_str(),
			}
		)
		print (savepath)
		# build the cline
		cli = BACKUP_CLI.format (
			exe=PYTHON_EXE,
			script=BACKUP_SCRIPT,
			encrypt= '-e %s' % encrypt if encrypt else '',
			log='-l %s' % log,
			type='-y %s' % t,
			saveas='-o %s' % savepath,
			url='-u %s' % s['url'],
			token='-t %s' % s['token'],
		)
		progress_msg ('Cline is %s ...' % cli)
		if os.system (cli):
			raise Exception ("failed to execute %s backup for '%s'" % (t, s['name']))



### MAIN

def main ():
	progress_msg ("Reading config file '%s' ..." % BACKUP_PARAMS)
	backup_params = read_db_list (BACKUP_PARAMS)
	sources = backup_params.get ('sources', None)
	assert sources, 'backup parameters do not list source databases'
	encrypt = str (backup_params.get ('encrypt', ''))
	log = backup_params.get ('log', LOG)
	saveas = backup_params.get ('saveas', SAVEAS)

	for s in sources:
		run_one_backup (s, encrypt, log, saveas)


if __name__ == '__main__':
	import sys
	main()
	sys.exit (0)


### END ###
