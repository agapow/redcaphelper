from setuptools import setup, find_packages
import sys, os

from redcaphelper import __version__

setup (
	name='redcaphelper',
	version=__version__,
	description="Utilities for working with the REDCap web database",
	long_description="""\
When working with a REDCap database, several regular tasks can become tedious -
uploading a large dataset in parts, backing up the data & schema, extracting
the latest import template. The package provides code fto help with these
routine tasks, allowing them to be easily scripted and automated. It heavily
leverages the PyCap package.""",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Information Technology',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Medical Science Apps.',
		'Topic :: System :: Archiving :: Backup',

	],
	keywords='database REDCap pycap',
	author='Paul Agapow & Kester Jarvis',
	author_email='paul@agapow.net',
	url='http://www.agapow.net/software/redcaphelper',
	license='MIT',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'pycap',
	],
	entry_points={
		'console_scripts': [
			'redcap-download = redcaphelper.scripts.download:main',
			'redcap-upload = redcaphelper.scripts.upload:main',
			'redcap-fill-template = redcaphelper.scripts.filltemplate:main',
			'redcap-make-vocab = redcaphelper.scripts.mkvocab:main',
		],
	},
)
