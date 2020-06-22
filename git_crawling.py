import requests
import git as g
from bs4 import BeautifulSoup
from models import User, Repository, File

def get_all_repositories(user: User, filter: object=None):
	repos = g.get_all_repositories(user.github_username)
	obj_repos = []
	for repo in repos:
		repo = g.repository_to_obj(repo, user.id)

		if filter:
			if not filter(repo): continue
		
		obj_repos.append(repo)

	return obj_repos

def get_all_files(repo: Repository, filter: object=None, branch='master'):
	files = []
	dirs = ['https://github.com/{}/tree/{}/'.format(repo.fullname, branch)]

	while dirs:
		url = dirs.pop(0)
		src = requests.get(url).text
		soup = BeautifulSoup(src, 'lxml')
		file_tags = soup.select('.files .js-navigation-item')

		for tag in file_tags:
			name = tag.select('.content a')[0].text
			commit_sha = tag.select('.message a')[0].attrs['href'][-40:]
			is_file = not tag.attrs['href'].startswith('/{}/tree'.format(repo.fullname))

			fullname = tag.attrs['href'].split('/{}/'.format(branch))[-1]
			file = File(
				fullname=fullname, name=name, 
				last_commit_sha=commit_sha, repo_fullname=repo.fullname
			)

			if filter:
				if not filter(file, is_file): continue

			if not is_file: # is directory
				dirs.append('https://github.com'+tag.attrs['href'])
			else:
				files.append(file)
				
	return files

def get_file_content(file: File, branch='master'):
	return requests.get(url = 'https://raw.githubusercontent.com/{}/{}/{}'.format(file.repo_fullname, branch, file.fullname)).text