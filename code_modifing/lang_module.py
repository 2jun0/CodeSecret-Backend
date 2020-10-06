import os
import sys
import git_crawling as gc
import db
from models import Repository, File
import re
import time

# 이 class가 초기화하는 것은 repository를 수정하겠다는 의미이다.
# 그러니까 초기화시 header 파일을 생성해도 된다.
class LangModule:
	def __init__(self, fork_repo: Repository, header_file_name, secret_keys_file, secret_keys_file_content, secret_key_cnt, gitignore_file: File):
		assert fork_repo.github_obj

		self.fork_repo:Repository = fork_repo
		self.header_file_name = header_file_name
		self.secret_keys_file = secret_keys_file
		self.secret_keys_file_content = secret_keys_file_content
		self.secret_key_cnt = secret_key_cnt
		self.gitignore_file:File = gitignore_file

	def modify_file(self, file:File, origin_content, keys):
		pass
	
	# secret key 개수는 파일에 Secret Key Count = 10 이런식으로 적혀짐
	def prepare_header_file(self):

		if not re.search('^{}$'.format(self.header_file_name), self.gitignore_file.content):
			modified_gitignore_content = self.gitignore_file.content + '\n' + self.header_file_name
			self.fork_repo.update_file(
				file=self.gitignore_file,
				title='Secret key leak fix',
				content=modified_gitignore_content,
				branch='code-fix')
		
	def get_header_file_fullname(self):
		return self.fork_repo.fullname+'/'+self.header_file_name