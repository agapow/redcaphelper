from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='redcaphelper',
      version=version,
      description="Utilities for working with the REDCap database",
      long_description="""\
It's useful to programatically work with the REDCap database, e.g. for uploading or downloading data via scripts. This package builds upon the functionality of the redcap package, to expand upon""",
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
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
