"""
Utils to work with vocabularies / choices.
"""

### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()


### CONSTANTS & DEFINES

### CODE ###

def build_vocab_str (choice_prs):
   """
   Args:
      - choice_prs (sequence): a list of pairs '(value, name)'

   Returns: a string

   """
   choice_strs = ['%s, %s' % (x[0], x[1]) for x in choice_prs]
   return ' | '.join (choice_strs)
