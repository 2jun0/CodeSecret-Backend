import git as g
import git_crawling as gc
from filters import file_filter

g.init()

import timeit

repos = g.get_all_repositories('2jun0')
for repo in repos:
	print(g.get_lastest_commit_sha(repo))

pin2 = timeit.default_timer()
pin = timeit.default_timer()
# for repo in repos:
# 	print('------------')
# 	print(timeit.default_timer() - pin)
# 	pin = timeit.default_timer()

# 	r = repository_to_obj(repo, None)
# 	files = gc.get_all_files(r, file_filter)
# 	for file in files:
# 		print(file.fullname)

# 	print(timeit.default_timer() - pin)
# 	pin = timeit.default_timer()

print('걸린 시간 : ', timeit.default_timer() - pin2)

