import time
import hashlib
import config
import github
import git as g
import git_crawling as gc
import re
import db
from models import Repository, File, SecretKey
from .python_lang_module import PythonLangModule
from .javascript_lang_module import JavascriptLangModule
from .c_lang_module import CLangModule
from .java_lang_module import JavaLangModule

# 이 클래스는 재활용하면 안된다. repo가 고정되어있기 때문이다 (변경 불가능)
class CodeModifier:

	def __init__(self, upstream_repo:Repository, files=None):
		assert upstream_repo.github_obj

		self.is_prepared = False
		self.upstream_repo:Repository = upstream_repo
		self.files = files
		self.fork_repo:Repository = None
		self.lang_module_dict = dict() # 이 언어 모델은 LangModule을 상속하고, 파일 수정, 헤더파일 수정에 쓰인다.

	# 준비는 한번만 할 수 있음.
	# 코드를 수정할 fork 저장소, code-fix 브랜치를 만든다.
	def prepare(self):
		assert self.is_prepared == False
		self.is_prepared = True

		self.fork_upstream_repo()

		# check gitignore file
		gitignore_file_dict = db.get_file('.gitignore')
		if gitignore_file_dict:
			self.gitignore_file = db.file_dict_to_obj(gitignore_file_dict)
			self.gitignore_file.content = gc.get_file_content(self.gitignore_file)
		# 없으면 생성
		else:
			# 헤더 파일 내용
			self.gitignore_file = self.fork_repo.create_file('.gitignore', 'Secret key leak fix', '', branch='code-fix')
			self.gitignore_file.content = ''

	# 파일을 수정한다.
	def modify_file(self, file:File, origin_content:str, keys:list):
		try:
			if not self.is_prepared:
				self.prepare()

			# TODO 파일 수정하는 코드 넣어줘!
			if file.fullname.endswith('.py'):
				if 'py' not in self.lang_module_dict:
					self.lang_module_dict['py'] = PythonLangModule(self.fork_repo, self.gitignore_file)
				self.lang_module_dict['py'].modify_file(file, origin_content, keys)
			elif file.fullname.endswith('.js'):
				if 'js' not in self.lang_module_dict:
					self.lang_module_dict['js'] = JavascriptLangModule(self.fork_repo, self.gitignore_file)

				self.lang_module_dict['js'].modify_file(file, origin_content, keys)
			elif file.fullname.endswith('.c') or file.fullname.endswith('.cpp'):
				if 'c' not in self.lang_module_dict:
					self.lang_module_dict['c'] = CLangModule(self.fork_repo, self.gitignore_file)

				self.lang_module_dict['c'].modify_file(file, origin_content, keys)
			elif file.fullname.endswith('.java'):
				if 'java' not in self.lang_module_dict:
					self.lang_module_dict['java'] = JavaLangModule(self.fork_repo, self.gitignore_file)

				self.lang_module_dict['java'].modify_file(file, origin_content, keys)
			else:
				return
		except Exception as e:
			self.fork_repo.github_obj.delete()
			self.fork_repo.github_obj = None
			raise e
		

	def pull_request(self):
		if self.fork_repo:
			pull = self.upstream_repo.github_obj.create_pull("[Code Secret] Secret key leak problem fix", "Secret key leak problem fix", "master", "{}:code-fix".format(config.GITHUB_ACCOUNT['username']), True)
			print('pull request : ', pull)
			self.fork_repo.github_obj.delete()
			self.fork_repo = None

			return pull

	# upstream을 포크해서 code-fix 브랜치를 만든다.
	def fork_upstream_repo(self):
		# fork
		self.fork_repo = g.repository_to_obj(repo = self.upstream_repo.github_obj.create_fork(), owner = config.GITHUB_ACCOUNT['username'])
		
		# create code-fix branch
		refs = self.fork_repo.github_obj.get_git_refs()

		code_fix_ref = None
		gobj_master_ref = None

		for ref in refs:
			if ref.ref == 'refs/heads/master':
				gobj_master_ref = ref
			elif ref.ref == 'code_fix_ref':
				code_fix_ref = ref
				
		if not code_fix_ref:
			self.fork_repo.github_obj.create_git_ref('refs/heads/code-fix', gobj_master_ref.object.sha)
