"""
Nosetests for redcaphelper/connection.py
"""

class TestConnection (object):
	def setup (self):
		import os
		from redcaphelper import Connection

		url = os.environ['REDCAPHELPER_TEST_URL']
		token = os.environ['REDCAPHELPER_TEST_TOKEN']
		self.conn = Connection (url, token)

	def teardown (self):
		pass
