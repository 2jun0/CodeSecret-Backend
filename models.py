class User:
	def __init__(self, id, password, github_username, github_obj=None):
		self.id = id
		self.password = password
		self.github_username = github_username
		self.github_obj = github_obj

class File:
	def __init__(self, fullname, name, last_commit_sha, repo_fullname, sha, github_obj=None, content=None):
		self.fullname = fullname
		self.name = name
		self.last_commit_sha = last_commit_sha
		self.repo_fullname = repo_fullname
		self.sha = sha
		self.github_obj = github_obj
		self.content = content # special value (db에 포함되지 않음)

class Repository:
	def __init__(self, fullname, name, last_commit_date, last_commit_sha, owner, github_obj=None):
		self.fullname = fullname
		self.name = name
		self.last_commit_date = last_commit_date
		self.last_commit_sha = last_commit_sha
		self.owner = owner
		self.github_obj = github_obj
		self.upstream_repo = None

	def update_file(self, file: File, title: str, content: str, branch: str):
		assert self.github_obj
		
		# 파일 업데이트 실행
		result = self.github_obj.update_file(file.fullname, title, content, sha=file.sha, branch=branch)
		commit = result['commit']
		content_file = result['content']

		# 파일 정보 업데이트
		file.sha = content_file.sha
		file.last_commit_sha = commit.sha
		file.content = content

	def create_file(self, file_fullname: str, title: str, content: str, branch: str):
		assert self.github_obj

		# 파일 생성
		result = self.github_obj.create_file(file_fullname, title, content, branch=branch)
		commit = result['commit']
		content_file = result['content']

		# 파일 객체 생성
		new_file = File(
			fullname=file_fullname,
			name=content_file.name,
			last_commit_sha=commit.sha,
			repo_fullname=self.fullname,
			sha=content_file.sha,
			content=content)

		return new_file

class SecretKey:
	def __init__(self, y, x, file_fullname, file_commit_sha, content, repo_last_commit_sha=None, pull_num=0, github_obj=None):
		self.y = y
		self.x = x
		self.file_fullname = file_fullname
		self.file_commit_sha = file_commit_sha
		self.content = content
		self.github_obj = github_obj
		self.repo_last_commit_sha = repo_last_commit_sha
		self.pull_num = pull_num
