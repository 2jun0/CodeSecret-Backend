from models import User

import git as g
import db

from filters import file_filter, patern_finder, entropy_filter

db.init()
g.init()

# user = User('1234', 'encrypted_password', '2jun0')

# # 레파지토리의 파일 분석 및 소스코드 분석(스레드 실행)
# db.add_all_of_all_repositories(user=user, file_filter=file_filter, api_keys_finder=patern_finder,api_keys_filters=[entropy_filter])

# repo = g.get_g().get_repo("CodeSecretTeam/test")
upstream_repo = g.get_g().get_repo("2jun0/CodeSecret-Frontend")
repo = g.get_g().get_repo("CodeSecretTeam/CodeSecret-Frontend")
body = '''
SUMMARY
Change HTTP library used to send requests
TESTS
  - [x] Send 'GET' request
  - [x] Send 'POST' request with/without body
'''
# repo.create_fork()
# master_ref = repo.get_git_ref('heads/master')
# repo.create_git_ref('refs/heads/code-fix', master_ref.object.sha)
# for ref in repo.get_git_refs():
# 	print(ref)
# commit = repo.create_file('new file2', 'coomits', body, 'code-fix')
# print(commit)
pr = upstream_repo.create_pull("Use 'requests' instead of 'httplib'", body, "master", "CodeSecretTeam:code-fix", True)
print(pr)