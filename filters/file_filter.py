import re
from filters.filter_config import FILE_FILTER

import db
from models import File

ignore_regex = re.compile("({})".format('|'.join(FILE_FILTER['IGNORE_NAME'])))
extension_regex = re.compile('^.*\.({})$'.format('|'.join(FILE_FILTER['ALLOW_FILE_EXTENSIONS'])))

def file_filter(cur_file: File, is_file):
	if ignore_regex.search(cur_file.name):
		return False

	if not is_file:
		return True
	
	if not extension_regex.search(cur_file.name):
		return False
	
	prev_file = db.get_file(cur_file.fullname)

	if not prev_file:
		db.add_file(cur_file)
		return False
	
	prev_file = db.file_dict_to_obj(prev_file)
	if cur_file.last_commit_sha != prev_file.last_commit_sha:
		db.update_file(fullname=prev_file.fullname, last_commit_sha=cur_file.last_commit_sha)
		return False

	return True

import sys
sys.modules[__name__] = file_filter