import db
from models import Repository

def repo_filter(cur_repo: Repository, is_file):
	prev_repo = db.get_repository(cur_repo.fullname) # 이전 정보

	if not prev_repo:
		db.add_repository(cur_repo)
		return False

	prev_repo = db.repo_dict_to_obj(prev_repo)
	if cur_repo.last_commit_sha != prev_repo.last_commit_sha: # 이전과 최신의 정보가 다르다?!
		db.update_repository(fullname=prev_repo.fullname, last_commit_sha=cur_repo.last_commit_sha, last_commit_date=cur_repo.last_commit_date) # 저장소를 새 정보로 업데이트
		return False
	
	return True

import sys
sys.modules[__name__] = repo_filter