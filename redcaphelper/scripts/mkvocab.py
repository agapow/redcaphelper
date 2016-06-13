#!/usr/bin/env python

"""
Read input and transform lines into a vocabulary suitable for REDCap.
"""

### IMPORTS

import sys

import re


### CONSTANTS & DEFINES

SPACE_PATT = re.compile ('[]\s\.\-\:\/]+')


### CODE ###

def make_vc_value (vc_label):
	val_str = vc_label.lower().strip()
	val_str = SPACE_PATT.sub ('_', val_str)
	return val_str


for line in sys.stdin:
	vc_value = make_vc_value (line)
	print ("%s, %s | " % (vc_value, line.strip()))


### END ###
