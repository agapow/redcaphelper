"""
A live connection to a REDCap database.

This serves largely to wrap associated functionality around a PyCap connection,
mostly just for neatness.
"""

### IMPORTS

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import object

import csv

# Py2 vs py3
try:
	from StringIO import StringIO
except:
	from io import StringIO

import redcap

from . import consts
from . import utils
from . import csvutils

__all__ = [
	'Connection'
]


### CONSTANT & DEFINES

### CODE ###

class Connection (redcap.Project):
	"""
	A live connection to a REDCap database.

	Mostly just a wrapping of the PyCap interface, for neatness.
	"""

	def __init__ (self, url, token):
		"""
		Initialise connection to REDCap project.

		Args:
			url (str): URL of the database
			token (str): the long alphanumeric access string. Note that this is
				specific to a database and a user (and that user's permissions).

		For example::

			>>> import os
			>>> url = os.environ['REDCAPHELPER_TEST_URL']
			>>> token = os.environ['REDCAPHELPER_TEST_TOKEN']
			>>> conn = Connection (url, token)

		"""
		## Preconditions:
		assert url.startswith ('http'), \
			"redcap api url '%s' is deformed " % url
		assert url.endswith ('/'), \
			"redcap api url '%s' does not end in forward-slash" % url

		## Main:
		super (Connection, self).__init__ (url, token)

	def import_records_chunked (self, recs, chunk_sz=consts.DEF_UPLOAD_CHUNK_SZ,
			sleep=consts.DEF_SLEEP, overwrite=True):
		"""
		Import records into the attached database.

		Args:
			recs (sequence of dicts): data to be uploaded
			chunk_sz (int): number of records to be uploaded in each batch
			sleep (int): seconds to wait between each upload
			overwrite (bool): should values missing in the import be overwritten

		Importing is a memory- (and CPU-) hungry process for REDCap. Thus it is
		necessary to manually throttle the process by uploading data in chunks
		and pausing between chunks.

		"""
		# TODO(paul): exactly what does the overwrite arg do?
		# TODO(paul): print better response & handle reponses better
		# TODO(paul): have seperate upload_chunk function for better handling?
		# TODO(paul): need date format option?

		## Main:
		id_fld = self.def_field
		total_len = len (recs)

		for start, stop in utils.chunked_enumerate (recs, chunk_sz):
			msg = "Uploading records %s-%s of %s ('%s' to '%s')" % (
				start, stop-1, total_len, recs[start][id_fld], recs[stop-1][id_fld]
			)
			utils.msg_progress (msg)
			response = self.import_records (
				recs[start:stop],
				overwrite='overwrite' if overwrite else 'normal'
			)

			# XXX(paul): more informative messages
			utils.msg_progress (response)
			if sleep and (stop != total_len):
				time.sleep (sleep)

	def export_records_chunked (self,
			records=None, fields=None, forms=None, events=None,
			raw_or_label='raw', event_name='label', format='json',
			export_survey_fields=False, export_data_access_groups=False,
			df_kwargs=None, chunk_sz=consts.DEF_DOWNLOAD_CHUNK_SZ,
		):
		"""
		Download data in chunks to avoid memory errors.

		Args:
			chunk_sz (int): number of records to be downloaded in each batch
			format ('json', 'csv', 'dicts', 'xml', 'df'): the format of data to
				be returned

		Returns:
			a series of records in one format or another

		Only arguments peculiar to this function are detailed. See
		`export_records` for all others.

		Exporting is also a memory-hungry process for REDCap. Thus we make it
		easy on the server by batching up the downloaded records and combining
		them ourselves.

		"""
		# TODO(paul): combine chunking functions?
		# XXX(paul): dataframe export format should be easy and useful?

		## Preconditions & preparation:
		assert format in ('json', 'csv', 'dicts', 'xml', 'df'), \
			"unrecognised export format '%s'" % format

		## Main:
		# if downloading all records get list
		if not records:
			id_fld = self.def_field
			record_list = self.export_records (fields=[id_fld])
			records = [r[id_fld] for r in record_list]

		# work out download format
		dl_format = 'csv' if format in ('dicts') else format

		# now do the actual download
		try:
			responses = []
			total_len = len (records)

			for start, stop in utils.chunked_enumerate (records, chunk_sz):
				msg = "Downloading records %s-%s of %s ('%s' to '%s')" % (
					start+1, stop, total_len, records[start], records[stop-1]
				)
				utils.msg_progress (msg)

				chunked_response = self.export_records (
					records=records[start:stop],
					fields=fields,
					forms=forms,
					events=events,
					raw_or_label=raw_or_label,
					event_name=event_name,
					format=dl_format,
					export_survey_fields=export_survey_fields,
					export_data_access_groups=export_data_access_groups,
					df_kwargs=df_kwargs,
				)

				# TODO: need to handle all possible ways of extending data
				responses.append (chunked_response)

		except redcap.RedcapError:
			# XXX(paul): shouldn't we just raise the intial error
			msg = "Chunked export failed for chunk_size %s" % chunk_sz
			raise ValueError (msg)
		else:
			# combine all the responses: json, csv, dicts, xml, df
			combined_reponses = None
			if dl_format == 'csv':
				combined_reponses = ''.join (responses)
			if dl_format == 'json':
				combined_reponses = []
				for x in responses:
					combined_responses.extend (x)
			if dl_format == 'xml':
				pass
			if dl_format == 'df':
				pass

			# need to translate back into
			if format == 'dicts':
				response = csvutils.csv_str_to_dicts (combined_reponses)

			return combined_reponses

	def export_schema (self):
		"""
		Download the project schema (fields).

		The project object actually contains the project schema as metadata
		but in a slightly awkward format. This returns the schema as a series of
		dicts giving the fields and their various options like validation.

		These will be in the order they appear in the project.

		"""
		csv_txt = self.export_metadata (format='csv')
		return csvutils.csv_str_to_dicts (csv_txt)


	# def export_field_names (self):
	# 	"""
	# 	Download the project fields.
	#
	# 	These will be in the order they appear in the project. Remember that in
	# 	REDCap, IDs are "names" and titles are "labels".
	#
	# 	"""
	# 	return [r['Variable / Field Name'] for r in self.export_schema()]





### END ###
