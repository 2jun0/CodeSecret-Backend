import os
import sys
from models import File, Repository
import db
import git_crawling as gc
from .lang_module import LangModule
import re

class DefaultLangModule(LangModule):
	def __init__(self, fork_repo:Repository, header_file_name:str, gitignore_file:File):
		super().__init__(fork_repo, header_file_name, None, None, 0, gitignore_file)
		self.prepare_header_file()

	def _get_comment_str(self, s:str):
		return s

	def _get_import_str(self):
		return ''

	def _get_header_def(self, val_name:str):
		return '{} = "YOUR SECRET KEY"'.format(val_name)

	def _header_update(self, key_name:str):
		self.header_file.content += '{}\n'.format(self._get_header_def(key_name))

	def _get_init_header(self):
		return self._get_comment_str('Secret Key Count = {}\n'.format(self.secret_key_cnt))

	def modify_file(self, file:File, origin_content, keys):
		# 대상 key 수정, 파일수정
		## key들을 모두 SECRET_KEY_번호 방식으로 수정
		modified_content = origin_content
		key_vals = []
		for key in keys:
			if key.content not in key_vals:
				self.secret_key_cnt += 1
				
				key_name = 'SECRET_KEY_{}'.format(self.secret_key_cnt) # 새로 바꿀 변수

				self._header_update(key_name)
				modified_content = re.sub('[\'\"]{}[\'\"]'.format(key.content), key_name, modified_content)

			key_vals.append(key.content)
		
		# 헤더파일에서 #Secret Key Count 수정
		self.header_file.content = re.sub(
			self._get_comment_str('Secret Key Count = (\d+)'), 
			self._get_comment_str('Secret Key Count = {}'.format(self.secret_key_cnt)),
			self.header_file.content)

		# 헤더파일 import 추가
		modified_content = self._get_import_str() + '\n' + modified_content

		# 코드파일&헤더파일 수정된 내용 업데이트
		self.fork_repo.update_file(
			file = file, title = 'Secret key leak fix', 
			content = modified_content, branch='code-fix')
		self.fork_repo.update_file(
			file = self.header_file, title='Secret key leak fix',
			content = self.header_file.content, branch='code-fix')
		
	def prepare_header_file(self):
		super().prepare_header_file()
		file_fullname = self.get_header_file_fullname()

		header_file_dict = db.get_file(file_fullname)
		if header_file_dict:
			self.header_file = db.file_dict_to_obj(header_file_dict)
			self.header_file.content = gc.get_file_content(self.header_file)
			# secret key 개수는 파일에 #Secret Key Count = 10 이런식으로 적혀짐
			m = re.search(
				self._get_comment_str('Secret Key Count = (\d+)'),
				self.header_file.content)
			self.secret_key_cnt = int(m.group(0))
		else:
			# 헤더 파일 내용
			self.secret_key_cnt = 0
			content = self._get_init_header()

			self.header_file = self.fork_repo.create_file(
				file_fullname = self.header_file_name, title='Secret key leak fix',
				content = content, branch='code-fix')
