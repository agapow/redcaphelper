redcaphelper
============

Background
----------

REDCap is a fabulously useful tool for creating web databases, especially the
web API which allows the database to be manipulated via a REST API. the
``pycap`` module, written by Scott Burns. provides a friendly Python interface to work with this API.

In turn, ``redcaphelper`` wraps the ``pycap`` interface to provide some useful
functions (e.g. chunked uploads and downloads, downloading the database schema)
and some useful scripts that use these for uploads, backups as well as other
tasks like generating REDCap vocabularies and filling in import templates.


Using redcaphelper
------------------

Code API
~~~~~~~~

redcaphelper's principal functionality is provided in the Connection class. This wraps and provides all the functionality of the pycap Project class, plus a few extra, useful methods:

* ``import_records_chunked`` gives the ability to import data into REDCap as per the base class ``import_records`` but "chunks" the upload into smaller parts. The import process is very memory intensive and if too much data is sent, it will crash the server. By breaking the upload into smaller parts, uploads will be safely completed.

* While export is not as memory intensive, ``export_records_chunked`` provides an analogous service.

* ``export_schema`` downloads a copy of the data dictionary for the database.

Various other useful functions are provided, including::

* ``read_csv`` and ``write_csv`` for simple "one line" handling of csv data.

* ``write_redcap_csv`` for writing files suitable for REDCap data upload.

Look at the scripts for examples of how these functions may be called and used.




Scripts
~~~~~~~

Several of the scripts call for the database API url and token to be passed.



**redcap-download** can be used download the data or schema (data dictionary) for a REDCap database. This can be used in data analysis or routine backup. Usage::

	redcap-download [-h] [--version] [-u URL] [-t TOKEN] [-o OUTFILE]
	                       [-y {data,schema}]

	optional arguments:
	  -h, --help            show this help message and exit
	  --version             show program's version number and exit
	  -u URL, --url URL     url for download
	  -t TOKEN, --token TOKEN
	                        API token
	  -o OUTFILE, --outfile OUTFILE
	                        where the backup is to be saved
	  -y {data,schema}, --type {data,schema}
	                        download schema or data

**redcap-upload** uploads a dataset to a REDCap database. Usage::

	redcap-upload [-h] [--version] [-u URL] [-t TOKEN] [-c CHUNK_SIZE]
							[--overwrite] [--no-overwrite]
							infile

	download contents or schema of a REDCap database

	positional arguments:
	infile                file to be imported to redcap

	optional arguments:
	-h, --help            show this help message and exit
	--version             show program's version number and exit
	-u URL, --url URL     url for upload
	-t TOKEN, --token TOKEN
								API token
	-c CHUNK_SIZE, --chunk-size CHUNK_SIZE
								number of records to upload at a time (packet size)
	--overwrite
	--no-overwrite

Note the options ``chunk-size`` and ``overwrite``. Import is a typically memory intensive process for REDCap and large datasets can crash the server. By "chunking" into smaller packets, this can be avoided. The default "chunk" for REDCap is 100, but a good rule of thumb is to upload 1 million cells at a time.

By default, import completely overwrite anything with the same unique record id. If overwrite is off, then blank / empty fields will not overwrite populated ones. Overwriting is the default behaviour. 


**redcap-make-vocab** is a tool for use when designing REDCap schema. It either
reads every line of standard input or that of any files passed and converts
them into a suitable form for the choices for a REDCap radio, dropdown or
checkbox field. Usage is::

	redcap-make-vocab [-h] [--version] [-a] [infiles [infiles ...]]

	produce REDCap vocabularies for fields with choices

	positional arguments:
	  infiles

	optional arguments:
	  -h, --help      show this help message and exit
	  --version       show program's version number and exit
	  -a, --as-lines  produce output with an item per line

Vocabulary names (the internal or raw values) are produced by taking the visible
text or label, making it lowercase, stripping all non-alphanumerics and
converting internal whitespace to underscores.

The vocabs produced are suitable for pasting into a REDCap data dcitionary. If
the item-per-line form used in the online designer is desired, the ``-l`` flag
can be used.


References
----------

* `redcaphelper code repository <https://github.com/agapow/redcaphelper>`__

* `redcaphelper homepage <http://www.agapow.net/software/redcaphelper/>`__

* `PyCap <https://github.com/redcap-tools/PyCap>`__
