from models import File, Repository
from .default_lang_module import DefaultLangModule
import re

class JavaLangModule(DefaultLangModule):
	def __init__(self, fork_repo:Repository, gitignore_file:File):
		super().__init__(fork_repo, 'AASecretKeys.java', gitignore_file)

	def _get_comment_str(self, s:str):
		return '//{}'.format(s)

	def _get_import_str(self):
		return 'import {}.*'.format(self.header_file_name)

	def _get_header_def(self, val_name:str):
		return 'public static String {} = "YOUR SECRET KEY"\n'.format(val_name)

	def _header_update(self, key_name:str):
		self.header_file.content = re.sub('public class AASecretKeys\s*{', 'public class AASecretKeys {\n\t%s'%(self._get_header_def(key_name)), self.header_file.content)

	def _get_init_header(self):
		return super()._get_init_header() + 'public class AASecretKeys {\n}'