import pymysql
from config import DATABASE_CONFIG
from error import CustomError
# models
from models import User, File, Repository, SecretKey

conn = None

def init():
	global conn
	conn = pymysql.connect(host=DATABASE_CONFIG['host'], user=DATABASE_CONFIG['user'], password = DATABASE_CONFIG['password'], db=DATABASE_CONFIG['dbname'], charset='utf8')

# -------------- user ----------------
def add_user(u: User):
	global conn
	try:
		curs = conn.cursor(pymysql.cursors.DictCursor)
		#sql문 실행

		# githubUsername 중복 확인
		sql = "select * from account where githubUsername = %s"
		curs.execute(sql, (u.github_username))
		if curs.rowcount > 0:
			raise CustomError(error='USER_GITHUB_ACCOUNT_DUPLICATE', 
				msg='이미 등록된 깃허브 계정 입니다.', status=500)

		sql = 'insert into account(id, password, githubUsername) values(%s,%s,%s)'
		curs.execute(sql, (u.id, u.password, u.github_username))
		conn.commit()
	except pymysql.err.IntegrityError as e:
		raise CustomError(error='USER_DUPLICATE',
			msg='이미 가입되어 있는 아이디 입니다.', status=500)

def get_user(id):
	global conn
	curs = conn.cursor(pymysql.cursors.DictCursor)
	#sql문 실행
	sql = "select * from account where id = %s"
	curs.execute(sql, (id))
	#데이터 fetch
	return curs.fetchone()

def _get_all_user_cur(): # cursor를 반환함.
	global conn
	curs = conn.cursor(pymysql.cursors.SSDictCursor)
	#sql문 실행
	sql = "select * from account"
	curs.execute(sql)
	#데이터 fetch
	return curs

# -------------- repository ----------------
def add_repository(r: Repository):
   global conn
   try:
      curs = conn.cursor(pymysql.cursors.DictCursor)
      #sql문 실행
      sql = 'insert into repository(fullname,name,lastCommitDate, lastCommitSha,owner) values(%s,%s,%s,%s,%s)'
      curs.execute(sql, (r.fullname, r.name, r.last_commit_date, r.last_commit_sha, r.owner))
      conn.commit()
   except pymysql.err.IntegrityError as e:
      raise CustomError(error='REPOSITORY_DUPLICATE', status=500, exception=e)

def exists_repository(fullname):
	global conn
	curs = conn.cursor(pymysql.cursors.DictCursor)
	#sql문 실행
	sql = "select exists(select * from repository where fullname=%s)"
	curs.execute(sql, (fullname))
	return curs.fetchone()

def get_repository(fullname):
	global conn
	curs = conn.cursor(pymysql.cursors.DictCursor)
	#sql문 실행
	sql = "select * from repository where fullname=%s"
	curs.execute(sql, (fullname))
	return curs.fetchone()

def get_repositories_by_username(username):
	global conn
	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select * from repository where owner =%s"
	curs.execute(sql, (username))
	return curs.fetchall()

def update_repository(fullname, name=None, last_commit_date=None, last_commit_sha=None, owner=None):
	global conn
	try:
		curs = conn.cursor(pymysql.cursors.DictCursor)

		# sql문 조합
		sql = 'update repository set '
		args = []
		if name: 
			args.append(name)
			sql += 'name = %s,'
		if last_commit_date:
			args.append(last_commit_date)
			sql += 'lastCommitDate = %s,'
		if last_commit_sha:
			args.append(last_commit_sha)
			sql += 'lastCommitSha = %s,'
		if owner:
			args.append(owner)
			sql += 'owner = %s,'
		
		args.append(fullname)
		sql = sql[:-1] # 마지막 문자 자르기(, 때문)
		sql += ' where fullname = %s'

		#sql문 실행
		curs.execute(sql, args)
		conn.commit()
	except pymysql.err.IntegrityError as e:
		raise CustomError(error='REPOSITORY_UPDATE_ERROR', status=500, exception=e)

def _get_all_repository_cur(owner): # cursor를 반환함.
	global conn
	curs = conn.cursor(pymysql.cursors.SSDictCursor)
	#sql문 실행
	sql = "select * from repository where owner = %s"
	curs.execute(sql, (owner))
	#데이터 fetch
	return curs

# -------------- file ----------------
def add_file(f: File):
   global conn
   try:
      curs = conn.cursor(pymysql.cursors.DictCursor)
      #sql문 실행
      sql = 'insert into file(fullname,name,lastCommitSha,repoFullname,sha) values(%s,%s,%s,%s,%s)'
      curs.execute(sql, (f.fullname,f.name,f.last_commit_sha,f.repo_fullname,f.sha))
      conn.commit()
   except pymysql.err.IntegrityError as e:
      raise CustomError(error='File_DUPLICATE', status=500, exception=e)

def get_file(fullname, repo_fullname):
	global conn
	curs = conn.cursor(pymysql.cursors.DictCursor)
	#sql문 실행
	sql = "select * from file where fullname=%s"
	curs.execute(sql, (fullname))
	return curs.fetchone()

def update_file(fullname, name=None, last_commit_sha=None, repo_fullname=None, sha=None):
	global conn
	try:
		curs = conn.cursor(pymysql.cursors.DictCursor)

		# sql문 조합
		sql = 'update file set '

		args = []
		if name: 
			args.append(name)
			sql += 'name = %s,'
		if last_commit_sha:
			args.append(last_commit_sha)
			sql += 'lastCommitSha = %s,'
		if repo_fullname:
			args.append(repo_fullname)
			sql += 'repoFullname = %s,'
		if sha:
			args.append(sha)
			sql += 'sha = %s,'
		
		sql = sql[:-1] # 마지막 문자 자르기(, 때문)
		args.append(fullname)
		sql += ' where fullname = %s'

		#sql문 실행
		curs.execute(sql, args)
		conn.commit()
	except pymysql.err.IntegrityError as e:
		raise CustomError(error='FILE_UPDATE_ERROR', status=500, exception=e)

# -------------- secret_key ----------------
def add_secret_key(s: SecretKey):
   global conn
   try:
      curs = conn.cursor(pymysql.cursors.DictCursor)
      #sql문 실행
      sql = 'insert into secret_key(y,x,fileFullname,fileCommitSha,content,pullNum,repoLastCommitSha) values(%s,%s,%s,%s,%s,%s,%s)'
      curs.execute(sql, (s.y,s.x,s.file_fullname,s.file_commit_sha,s.content,s.pull_num,s.repo_last_commit_sha))
      conn.commit()
   except pymysql.err.IntegrityError as e:
      raise CustomError(error='SECRET_KEY_DUPLICATE', status=500, exception=e)

def update_secret_key(id, pull_num):
	global conn
	try:
		curs = conn.cursor(pymysql.cursors.DictCursor)

		# sql문 조합
		sql = 'update file set '

		args = []
		if name: 
			args.append(name)
			sql += 'name = %s,'
		if last_commit_sha:
			args.append(last_commit_sha)
			sql += 'lastCommitSha = %s,'
		if repo_fullname:
			args.append(repo_fullname)
			sql += 'repoFullname = %s,'
		if sha:
			args.append(sha)
			sql += 'sha = %s,'
		
		sql = sql[:-1] # 마지막 문자 자르기(, 때문)
		args.append(fullname)
		sql += ' where fullname = %s'

		#sql문 실행
		curs.execute(sql, args)
		conn.commit()
	except pymysql.err.IntegrityError as e:
		raise CustomError(error='SECRET_KEY_UPDATE_ERROR', status=500, exception=e)

def get_recent_secret_keys(repo: Repository):
	global conn

	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select s.* from file as f, repository as r, secret_key as s\
					where r.fullname = %s and f.repoFullname = r.fullname and s.fileFullname = f.fullname and s.repoLastCommitSha = %s"
	curs.execute(sql, (repo.fullname, repo.last_commit_sha))
	return curs.fetchall()

def get_recent_pull_num(repo: Repository):
	global conn

	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select count(*) as keyCount, s.pullNum from file as f, repository as r, secret_key as s\
					where r.fullname = %s and f.repoFullname = r.fullname and s.fileFullname = f.fullname and s.repoLastCommitSha = %s"
	curs.execute(sql, (repo.fullname, repo.last_commit_sha))
	return curs.fetchone()

def connection_close():
	global conn
	#connection 종료
	conn.close()

# *******************************************
# git_crawling.py 의존 함수
# *******************************************
import git_crawling as gc

def add_all_repositories(user: User, repo_filter: object=None):
	for repo in gc.get_all_repositories(user, repo_filter):
		add_repository(repo)

def add_all_of_all_repositories(user: User, repo_filter: object=None, file_filter: object=None, api_keys_finder: object=None, api_keys_filters: list=[]): #, repo_branch='master'):
	for repo in gc.get_all_repositories(user, repo_filter):
		add_repository(repo)
		for file in gc.get_all_files(repo, file_filter):
			add_file(file)

			# api key 찾기
			content = gc.get_file_content(file)
			api_keys = []

			if api_keys_finder:
				api_keys = api_keys_finder(file, content)

			for filter in api_keys_filters:
				api_keys = filter(api_keys)

			for api_key in api_keys:
				add_secret_key(SecretKey(api_key))

# *******************************************
# dict -> model obj
# *******************************************
def user_dict_to_obj(user_dict):
	return User(id=user_dict['id'], password=user_dict['password'], github_username=user_dict['githubUsername'])
def repo_dict_to_obj(repo_dict):
	return Repository(fullname = repo_dict['fullname'], name = repo_dict['name'], last_commit_date = repo_dict['lastCommitDate'], last_commit_sha = repo_dict['lastCommitSha'], owner= repo_dict['owner'])
def file_dict_to_obj(file_dict):
	return File(fullname = file_dict['fullname'], name = file_dict['name'], last_commit_sha = file_dict['lastCommitSha'], repo_fullname= file_dict['repoFullname'], sha= file_dict['sha'])
def secret_key_dict_to_obj(secret_key_dict):
	return SecretKey(x=secret_key_dict['x'], y=secret_key_dict['y'], file_fullname=secret_key_dict['fileFullname'], file_commit_sha=secret_key_dict['fileCommitSha'], content=secret_key_dict['content'], repo_last_commit_sha=secret_key_dict['repoLastCommitSha'], pull_num=secret_key_dict['pullNum'])