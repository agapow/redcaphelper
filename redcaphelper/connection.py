"""
A live connection to a REDCap database.

This serves largely to wrap associated functionality around a PyCap connection,
mostly just for neatness.
"""

### IMPORTS

import redcap

import .const
import .utils

__all__ = [
	'Connection'
]


### CONSTANT & DEFINES


### CODE ###

class Connection (object):
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
		self._proj = redcap.Project (url, token)

	def import_recs (self, recs, chunk_sz, sleep=const.DEF_SLEEP):
		"""
		Import records into the attached database.

		Args:

		For example::

		"""
		total_len = len (recs)
		for x in range (0, total_len, chunk_sz):
			start = x
			stop = min (total_len, x+chunk_sz)
			self.print_progress ("Uploading records %s-%s of %s" % (start, stop-1, total_len))
			response = self._proj.import_records (recs[start:stop], overwrite='overwrite')
			self.print_progress (response)
			if sleep and (stop != total_len):
				time.sleep (sleep)

	def export_recs (self, chunk_sz=200, flds=None):
		"""
		Download data in chunks to avoid memory errors.
		"""
		## Preconditions & preparation:
		flds = flds or self._proj.def_field

		## Main:
		def chunks(l, n):
			"""
			Yield successive n-sized chunks from list l
			"""
			for i in range (0, len(l), n):
				yield l[i:i+n]

		id_fld = self._proj.def_field
		record_list = self._proj.export_records (fields=[id_fld])
		records = [r[id_fld] for r in record_list]

		try:
			response = []
			for record_chunk in chunks (records, chunk_sz):
				chunked_response = project.export_records (records=record_chunk)
				response.extend (chunked_response)
		except redcap.RedcapError:
			msg = "Chunked export failed for chunk_size={:d}".format (chunk_sz)
			raise ValueError (msg)
		else:
			return response

	def export_schema (self):
		csv_txt = self._proj.export_metadata (format='csv')
		csv_rdr = csv.DictReader (io.StringIO (csv_txt))
		return [r for r in csv_rdr]



	def print_progress (self, msg):
		print (msg, '...')



### END ###