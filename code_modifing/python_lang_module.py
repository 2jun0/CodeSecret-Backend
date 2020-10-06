from models import File, Repository
from .default_lang_module import DefaultLangModule

class PythonLangModule(DefaultLangModule):
	def __init__(self, fork_repo:Repository, gitignore_file:File):
		super().__init__(fork_repo, '_secret_keys.py', gitignore_file)

	def _get_comment_str(self, s:str):
		return '#{}'.format(s)

	def _get_import_str(self):
		return 'from {} import *'.format(self.header_file_name)

	def _get_header_def(self, val_name:str):
		return '{} = \'YOUR SECRET KEY\'\n'.format(val_name)