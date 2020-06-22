from github import Github
from config import GITHUB_ACCOUNT
from error import CustomError
from models import Repository, File

g = None

def rate_limit():
	global g
	return g.get_rate_limit()

def init():
	global g
	g = Github(GITHUB_ACCOUNT['username'], GITHUB_ACCOUNT['password'])

def github_account_validate(github_username, github_password):
	try:
		g = Github(github_username, github_password)
		data = [(s.name, s.name) for s in g.get_user().get_repos()]
		return True
	except Exception as e:
		raise CustomError(error = 'INVALID_GITHUB_ACCOUNT', msg='깃허브 계정정보가 잘못되었습니다.', status=401)

# def exist_github_user(github_username):
# 	global g
# 	try:
# 		g.get_user(github_username)
# 		return True
# 	except Exception as e:
# 		return False

def get_repository(repository):
	global g
	return g.get_repo(repository)

def get_all_repositories(github_username):
	global g
	return g.get_user(github_username).get_repos()

# 아래 세개의 함수는 git_crawling에서도 정상적으로 동작하는 함수가 있으니, 왠만하면 git_crawling의 함수를 쓰십시오.
def get_all_files(repo):
	files = []
	contents =  repo.get_contents("")
	while contents:
		file_content = contents.pop(0)
		if file_content.type == 'dir':
			contents.extend(repo.get_contents(file_content.path))
		else:
			files.append(file_content)
	return files

def get_lastest_commit(repo):
	return repo.get_commits().get_page(0)[0].commit

def get_lastest_commit_date(repo):
	return get_lastest_commit(repo).author.date

def get_lastest_commit_sha(repo):
	return get_lastest_commit(repo).sha

# *******************************************
# pygithub obj -> model obj
# *******************************************
def repository_to_obj(repo, owner):
	return Repository(fullname = repo.full_name, name = repo.name, last_commit_date = get_lastest_commit_date(repo), last_commit_sha = get_lastest_commit_sha(repo), owner=owner)

# *******************************************
# 테스트 전용 함수
# *******************************************
def get_g():
	global g
	return g