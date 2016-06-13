"""
Very assorted utilities and odds and ends for use in module.
"""

### IMPORTS

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from builtins import range

__all__ = [
	'msg_progress',
	'chunked_enumerate',
]


### CONSTANTS & DEFINES

### CODE ###

## Chunking
# For use where we have to iterate over records in blocks, such as downloading.
# Or uploading. Oh, REDCap, you scamp.


def chunked_enumerate (seq, chunk_sz):
	"""
	Yield successive n-sized chunks from l, as indices

	Args:
		seq (seq): the collection to be iterated over
		chunk_sz (int): the size or index 'jump' for each chunk

	Returns:
		yields the start and stop indices of each chunk

	This allows us to iterate over large sequences in pieces. Note that this
	doesn't return the actual elements but their indices. This allows us to
	track and post progress.

	"""
	## Preconditions:
	assert 0 < n, "chunk size '%s' must be greater than 0" % chunk_sz

	## Main:
	total_len = len (seq)
	for i in range (0, len (seq), chunk_sz):
		start = i
		stop = min (total_len, i+chunk_sz)
		yield start, stop



## Messaging

def msg_progress (msg, end=False):
	"""
	Print some diagnostic messages showing that things are happening.

	Args:
		msg (str): a message to print out to the console
		end (bool): end this message with a full stop?

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


## String formatting
# XXX: get rid of all this fomratting shit?

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
