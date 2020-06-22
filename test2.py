from models import User

import git as g
import db
import hashlib

from filters import file_filter, patern_finder, entropy_filter

db.init()
g.init()

# user = User('1234', 'encrypted_password', '2jun0')

# # 레파지토리의 파일 분석 및 소스코드 분석(스레드 실행)
# db.add_all_of_all_repositories(user=user, file_filter=file_filter, api_keys_finder=patern_finder,api_keys_filters=[entropy_filter])

upstream_repo = g.get_g().get_repo("2jun0/CodeSecret-Frontend")
# repo = g.get_g().get_repo("CodeSecretTeam/CodeSecret-Frontend")

repo = upstream_repo.create_fork()
# master_ref = repo.get_git_ref('heads/master')
# repo.create_git_ref('refs/heads/code-fix', master_ref.object.sha)

body = 'haha\ni am back2'
path = 'README.md'
# commit = repo.update_file(path, 'coomits', body, sha=hashlib.sha1(path.encode('utf-8')).hexdigest(), branch='code-fix')
# commit = repo.delete_file()
commit = repo.update_file(path, 'coomits', body, sha='08e599df20f4348a8e3a873bd53ebfbde6785d11', branch='code-fix')
print(commit)

# repo.delete()

# pr = upstream_repo.create_pull("Use 'requests' instead of 'httplib'", body, "master", "CodeSecretTeam:code-fix", True)
# print(pr)


# repo = g.get_g().get_repo("CodeSecretTeam/test")
# repo.create_fork()
# master_ref = repo.get_git_ref('heads/master')
# repo.create_git_ref('refs/heads/code-fix', master_ref.object.sha)
# for ref in repo.get_git_refs():
# 	print(ref)
