import time
from selenium import webdriver
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
		driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
		driver.get(url)

		html = driver.page_source
		while 'Skeleton' in html:
			time.sleep(0.1)
			html = driver.page_source

		soup = BeautifulSoup(html, 'lxml')
		file_tags = soup.select('.repository-content .js-navigation-item')

		for tag in file_tags:
			file_tag = tag.select('span a')
			if len(file_tag) == 0:
				continue

			file_tag = file_tag[0]

			name = file_tag.text
			file_sha = file_tag.attrs['id'].split('-')[-1]
			commit_sha = tag.select('.commit-message a')[0].attrs['href'][-40:]
			is_file = not file_tag.attrs['href'].startswith('/{}/tree'.format(repo.fullname))

			fullname = file_tag.attrs['href'].split('/{}/'.format(branch))[-1]
			file = File(
				fullname=fullname, name=name, 
				last_commit_sha=commit_sha, repo_fullname=repo.fullname, sha=file_sha
			)

			if filter:
				if not filter(file, is_file): continue

			if not is_file: # is directory
				dirs.append('https://github.com'+file_tag.attrs['href'])
			else:
				files.append(file)

		driver.quit()
				
	return files

def get_file_content(file: File, branch='master'):
	return requests.get(url = 'https://raw.githubusercontent.com/{}/{}/{}'.format(file.repo_fullname, branch, file.fullname)).text