from models import File, Repository
from .default_lang_module import DefaultLangModule

class JavascriptLangModule(DefaultLangModule):
	def __init__(self, fork_repo:Repository, gitignore_file:File):
		super().__init__(fork_repo, '_secret_keys.js', gitignore_file)

	def _get_comment_str(self, s:str):
		return '//{}'.format(s)

	def _get_import_str(self):
		return 'import * from {}'.format(self.header_file_name)

	def _get_header_def(self, val_name:str):
		return 'var {} = "YOUR SECRET KEY";\n'.format(val_name)