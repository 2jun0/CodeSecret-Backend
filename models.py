class User:
	def __init__(self, id, password, github_username):
		self.id = id
		self.password = password
		self.github_username = github_username

class Repository:
	def __init__(self, fullname, name, last_commit_date, last_commit_sha, owner):
		self.fullname = fullname
		self.name = name
		self.last_commit_date = last_commit_date
		self.last_commit_sha = last_commit_sha
		self.owner = owner

class File:
	def __init__(self, fullname, name, last_commit_sha, repo_fullname, sha):
		self.fullname = fullname
		self.name = name
		self.last_commit_sha = last_commit_sha
		self.repo_fullname = repo_fullname
		self.sha = sha

class SecretKey:
	def __init__(self, y, x, fileFullname, content):
		self.y = y
		self.x = x
		self.fileFullname = fileFullname
		self.content = content