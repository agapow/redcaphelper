"""
Very assorted utilities and odds and ends for use in module.
"""

### IMPORTS

from __future__ import print_function
from builtins import next

__all__ = [
	'msg_progress',
	'read_csv',
	'write_csv',
	'read_import_template',
	'write_redcap_csv',
]


### CONSTANTS & DEFINES

### CODE ###

## Messaging

def msg_progress (msg, end=False):
	"""
	Print some diagnostic messages showing that things are happening.

	"""
	# XXX(paul): this is balls, probably needs to be replaced with
	# decent messaging /logging or at least something with configurable
	# verbosity
	# XXX(paul): need a msg_error / msg_info / etc.
	if end:
		suffix = '.'
	else:
		suffix = ' ...'
	print ('%s%s' % (msg, suffix))


## IO: Manipulating CSV files

def read_csv (in_file):
	"""
	Slurp in the contents of a CSV file as a series of dicts.
	"""
	with open (in_file, 'rU') as in_hndl:
		rdr = csv.DictReader (in_hndl)
		return [r for r in rdr]


def write_csv (recs, out_file, hdr_flds=None, sort_on=None):
	"""
	Write a set of records to a CSV file.

	Records are sorted on the field passed Extra fields are ignored, fields
	that are not supplied are filled with an empty string.
	"""
	## Preconditions & preparation:
	if sort_on:
		recs = sorted (recs, key=lambda x: x[sort_on])
	if hdr_flds is None:
		hdr_flds = list(recs[0].keys())

	## Main:
	with open (out_file, 'w') as out_hndl:
		wrtr = csv.DictWriter (out_hndl, fieldnames=hdr_flds,
			extrasaction='ignore', restval='')
		wrtr.writeheader()
		wrtr.writerows (recs)


## IO: REDCap files

def read_import_template (in_file):
	"""
	Get the header fields (and their order) from import template.
	"""
	with open (in_file, 'rU') as in_hndl:
		fields_rdr = csv.reader (in_hndl)
		# there's a blank column in import file for unknown reasons
		# get rid of it
		hdr = [h for h in next(fields_rdr) if h]
		return hdr


def write_redcap_csv (recs, out_file, hdr_flds):
	"""
	Write a set of records to a CSV file suitable for REDCap upload.

	Records are sorted on the first field in the headers (which is assumed to
	be the subject number / id). Extra fields are ignored, fields that are not
	supplied are filled with an empty string.
	"""
	## Precondtions & prep:
	# check what fields aren't being written
	all_rec_fields = []
	for r in recs:
		all_rec_fields.extend (list(r.keys()))
	all_rec_fields = set (all_rec_fields)

	long_fields = [f for f in all_rec_fields if 26 < len (f)]
	if long_fields:
		print ('WARNING: the following fields are longer than 26 characters: %s' \
			% ', '.join (sorted (long_fields)))

	extra_exp_fields = [f for f in all_rec_fields if f not in hdr_flds]
	if extra_exp_fields:
		print ('WARNING: the following fields are in the converted records but' \
					'not the import template: %s' % ', '.join (sorted (extra_exp_fields)))

	extra_imp_fields = [f for f in hdr_flds if f not in all_rec_fields]
	if extra_imp_fields:
		print ('WARNING: the following fields are in the import template but'
			'not any of the converted records: %s' % ', '.join (sorted (extra_imp_fields)))

	## Main:
	# actually write stuff out
	write_csv (recs, out_file, hdr_flds, sort_on=hdr_flds[0])


## IO: other

def write_yaml (recs, out_file, hdr_flds=None, sort_on=None):
	## Preconditions & preparation:
	if sort_on:
		recs = sorted (recs, key=lambda x: x[sort_on])
	if hdr_flds is None:
		hdr_flds = list(recs[0].keys())

	## Main:
	from yaml import load, dump
	try:
		 from yaml import CLoader as Loader, CDumper as Dumper
	except ImportError:
		 from yaml import Loader, Dumper

	with open (out_file, 'w') as out_hndl:
		output = dump (recs, out_hndl, Dumper=Dumper)


## String formatting

def safe_format (s, mapping, def_mapping=True):
	"""
	Fill in a string template, allowing for missing keys.

	This is intended for use in constructng file names, especially in scripts.
	As opposed to the normal substitution or standard string ormatting, keys
	can can be missing. This means that strings can be formatted in stages,
	i.e. put one set of keys in, then another.
	"""
	import string
	t = string.Template (s)
	if def_mapping:
		mapping = default_format_mapping().update (mapping)
	return t.safe_substitute (mapping)


def safe_format_file (s, mapping, fpath):
	"""
	Construct a filename from a string template.

	Extract values from the file name / path and use them to safe formt a
	"""
	file_map = default_file_format_mapping (fpath)
	file_map.update (mapping)
	return safe_format (s, file_map)


def default_format_mapping():
	"""
	Default values to use in formatting template strings.
	"""
	from datetime import datetime
	now = datetime.now()

	def_map = {
		"date": now.strftime ("%Y%m%d"),
		"time": now.strftime ("%H%M%S"),
		"datetime": now.strftime ("%Y%m%dT%H%M%S"),
	}

	return def_map


def default_file_format_mapping (fpath):
	"""
	Default values to use in formatting template strings based on file names.
	"""
	import os.path as op

	# extract file dir and name
	pdir, pname = op.split (fpath)
	if (pdir and (not pdir.endswith (op.sep))):
		pdir += op.sep

	# exttact file base/stem and ext
	pstem, pext = op.splitext (pname)

	file_map = {
		"path": fpath,
		"dir": pdir,
		"name": pname,
		"base": pbase,
		"ext": pext,
	}

	return file_map


### END ###
