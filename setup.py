from setuptools import setup, find_packages
import sys, os

from redcaphelper import __version__

setup(
	name='redcaphelper',
	version=version,
	description="Utilities for working with the REDCap database",
	long_description="""\
	It's useful to programatically work with the REDCap database. This package
	builds upon the redcap package, to provide facilities for easy uploading or
	downloading data via scripts. """,
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='database REDCap pycap',
	author='Paul Agapow & Kester Jarvis',
	author_email='paul@agapow.net',
	url='http://www.agapow.net/software/redcaphelper',
	license='MIT',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'redcap',
	],
	entry_points="""
		# -*- Entry points: -*-
	""",
)
