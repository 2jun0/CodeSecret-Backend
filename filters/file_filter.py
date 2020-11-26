import re
from filters.filter_config import FILE_FILTER

import db
from models import File

ignore_regex = re.compile("({})".format('|'.join(FILE_FILTER['IGNORE_NAME'])))
extension_regex = re.compile('^.*\.({})$'.format('|'.join(FILE_FILTER['ALLOW_FILE_EXTENSIONS'])))

def file_filter(cur_file: File, is_file): # true가 우리가 찾는 파일 or 그냥 폴더
	if cur_file.name not in FILE_FILTER['SELECT_NAME']:
		if ignore_regex.search(cur_file.name):
			return False

		if not is_file:
			return True
		
		if not extension_regex.search(cur_file.name):
			return False
	
	prev_file = db.get_file(cur_file.fullname, cur_file.repo_fullname)

	if not prev_file: # db에 파일이 기록되지 않음
		db.add_file(cur_file)
		return True
	
	prev_file = db.file_dict_to_obj(prev_file)
	if cur_file.sha != prev_file.sha: # db에 파일이 기록됨 -> 업데이트 되었는가?
		db.update_file(fullname=prev_file.fullname, sha=cur_file.sha)
		return True

	return False

import sys
sys.modules[__name__] = file_filter

# if cur_file.last_commit_sha != prev_file.last_commit_sha: # db에 파일이 기록됨 -> 업데이트 되었는가?
# 		db.update_file(fullname=prev_file.fullname, last_commit_sha=cur_file.last_commit_sha)
# 		return True