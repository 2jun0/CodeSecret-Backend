import time
import threading
import db
import git as g
import git_crawling as gc
from models import User, SecretKey, Repository

from filters import repo_filter, file_filter, patern_finder, entropy_filter
from code_modifing.code_modifier import CodeModifier

running = True

def start(sleep_time):
	thr = threading.Thread(target = act, kwargs={'sleep_time':sleep_time})
	thr.start()

# 하나의 저장소에 있는 key 찾아서 수정
def act_for_one_repo(repo: Repository):
	code_modifier = CodeModifier(upstream_repo = repo)
	is_find = False

	for file in gc.get_all_files(repo, file_filter):
		# secret key 찾기
		content = gc.get_file_content(file)
		
		secret_keys = patern_finder(file, content)
		secret_keys = entropy_filter(secret_keys)

		# Key find
		if len(secret_keys) > 0:
			is_find = True

			# modify a file
			code_modifier.modify_file(file, content, secret_keys)

			for secret_key in secret_keys:
				visible_secret_key_len = int(len(secret_key.content)/2)
				secret_key.content = secret_key.content[:visible_secret_key_len] + '*'*(len(secret_key.content) - visible_secret_key_len)

				#??#db.add_secret_key(secret_key)

	if is_find:
		code_modifier.pull_request()

# 한명의 모든 저장소에 있는 key 찾아서 수정
def act_for_one_user(user: User):
	for repo in gc.get_all_repositories(user, repo_filter):
		act_for_one_repo(repo)

def act(sleep_time):
	global running

	while running:
		all_user_cur = db._get_all_user_cur()

		for user_dict in all_user_cur.fetchall():
			user = db.user_dict_to_obj(user_dict)
			act_for_one_user(user)

		time.sleep(sleep_time)

def stop():
	global running
	running = False