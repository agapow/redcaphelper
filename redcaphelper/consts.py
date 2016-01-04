"""
Module-wide constants.

"""

### IMPORTS

__all__ = [
	'DEF_SLEEP',
	'DEF_UPLOAD_CHUNK_SZ',
	'DEF_DOWNLOAD_CHUNK_SZ',
	'SCHEMA_FLD_ORDER',
]


### CONSTANTS & DEFINES

DEF_SLEEP = 1

DEF_UPLOAD_CHUNK_SZ = 100

DEF_DOWNLOAD_CHUNK_SZ = 100

SCHEMA_FLD_ORDER = [
	'field_name',
	'form_name',
	'section_header',
	'field_type',
	'field_label',
	'select_choices_or_calculations',
	'field_note',
	'text_validation_type_or_show_slider_number',
	'text_validation_min',
	'text_validation_max',
	'identifier',
	'branching_logic',
	'required_field',
	'custom_alignment',
	'question_number',
	'matrix_group_name',
	'matrix_ranking',
]



### END ###
