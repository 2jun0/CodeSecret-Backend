import hashlib
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
import git as g
from model import Respository, File, SecretKey

def fork_code(upstream_repo):
	# fork
	fork_repo = upstream_repo.create_fork()

	# crate code-fix branch
	master_ref = fork_repo.get_git_ref('heads/master')
	fork_repo.create_git_ref('refs/heads/code-fix', master_ref.object.sha)

	return fork_repo

def modify_code(upstream_repo: Respository, file:File, origin_content, keys:list):
	fork_repo = fork_code()

	repo.update_file('new file2', 'Secret key leak fix', body, sha=file.sha, branch='code-fix')

	pr = pull_request(upstream_repo, fork_repo)
	fork_repo.delete()

	return pr

def pull_request(upstream_repo, fork_repo):
	return upstream_repo.create_pull("[Code Secret] Secret key leak problem fix", "", "master", "{}:code-fix".format(config.GITHUB_ACCOUNT['username']), True)