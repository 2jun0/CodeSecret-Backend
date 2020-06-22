import time
import threading
import db
import git as g
import git_crawling as gc
from models import User, SecretKey

from filters import repo_filter, file_filter, patern_finder, entropy_filter

running = True

def start(sleep_time):
	thr = threading.Thread(target = act, kwargs={'sleep_time':sleep_time})
	thr.start()

def act(sleep_time):
	global running

	while running:
		all_user_cur = db._get_all_user_cur()

		for user_dict in all_user_cur:
				user = db.user_dict_to_obj(user_dict)

				for repo in gc.get_all_repositories(user, repo_filter):
					for file in gc.get_all_files(repo, file_filter):
						# api key 찾기
						content = gc.get_file_content(file)
						api_keys = []
						
						api_keys = patern_finder(file, content)
						api_keys = entropy_filter(api_keys)

						for api_key in api_keys:
							db.add_secret_key(SecretKey(api_key))

		time.sleep(sleep_time)

def stop():
	global running
	running = False