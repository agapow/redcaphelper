"""
Given a set of CSV records and the import template for a REDCap database,
format the records appropriately.
"""

#IMPORTS

import pandas
import csvutils


def fill_template(records, template):
	#???: KJ - Should this stay here or be moved into the general csvutils module? csvutils is more clean,
	#but leaving it here means pandas doesn't get loaded unnecessarily every time csvutils is used.
	"""
	Uses pandas update method to fill in a template empty data frame with the data in records, while
	retaining only the template columns. Extra columns in records but not in the template will be lost;
	columns in template but not in the passed record will be filled with blanks (NaN).
	"""
	filltemplate = pandas.DataFrame(template)
	filltemplate = filltemplate.reindex(records.index)
	filltemplate.update(records)
	return filltemplate


def parse_clargs (clargs):
    import argparse
    aparser = argparse.ArgumentParser()

    aparser.add_argument ("csvfile",
      	help='CSV file to be imported to template',
    )

    aparser.add_argument ("template",	#???: KJ - Should this be taken direct from RedCap
   		help='CSV template from RedCap')		  #instead of provided locally?

    aparser.add_argument("outfile",
		help='Name of the file you want to output to')
	
    aparser.add_argument("-t", "--transpose",
   		help='Does the table need transposing? (i.e. are ID numbers in a single row rather than single column?)',
   		type=bool
   		default=False)
	)

   args = aparser.parse_args()

   return args

def main(clargs):	#Need args: template (template csv file), records (record CSV file)
	import sys
	args = parse_clargs(clargs)
	with open(args.csvfile, 'r') as in_hndl:
		records = pandas.read_csv(in_hndl, index_col = 0)
	with open(args.template, 'r') as in_hndl2:
		template = pandas.read_csv(in_hndl2, index_col = 0)
	if args.transpose:
		records = records.transpose()
	filledtemplate = fill_template(records, template)
	with open(args.outfile, 'w') as out_hndl:	#???: KJ - do we want to make this upload to REDCap instead?
		filledtemplate.to_csv(out_hndl, na_rep=None)

if __name__ == '__main__':
	main (sys.argv[1:])


