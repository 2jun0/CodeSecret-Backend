from models import File, Repository
from .default_lang_module import DefaultLangModule

class CLangModule(DefaultLangModule):
	def __init__(self, fork_repo:Repository, gitignore_file:File):
		super().__init__(fork_repo, '_secret_keys.h', gitignore_file)

	def _get_comment_str(self, s:str):
		return '//{}'.format(s)

	def _get_import_str(self):
		return '#include "{}"'.format(self.header_file_name)

	def _get_header_def(self, val_name:str):
		return '#define {}\t"YOUR SECRET KEY"'.format(val_name)
