import atexit
import sys
# import threading
from flask import Flask, request, session, Response, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity, get_jwt_claims)
from flask_cors import CORS

import db
import git_crawling as gc
import git as g
import secret_key_finder as skf
from models import User
from config import APP_CONFIG
from error import CustomError

app = Flask(__name__)
CORS(app)
app.secret_key = APP_CONFIG['secret_key']

db.init()
g.init()
skf.start(600)

app.run(host='localhost')

@app.route('/')
def hello_route():
	return 'hello, route!'

# start - 암호화를 위한 bcrypt 세팅 코드
app.config['SECRET_KEY'] = APP_CONFIG['bcrypt_secret_key']
app.config['BCRYPT_LEVEL'] = APP_CONFIG['bcrypt_level']
bcrypt = Bcrypt(app)
# end - bcrypt 세팅 코드
# ---------------------------------------------
# start - 계정 관련 코드
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login_route():
	try:
		id = request.json['id']
		password = request.json['password']
		user = db.get_user(id) # db에서 계정정보 가져오기

		# password에는 암호화가 적용되어있기 때문에 이렇게 해야함.
		if user is None:
			raise CustomError(error='LOGIN_ID_UNDEFINED', msg='해당 아이디가 존재하지 않습니다.', status=401)
		elif not bcrypt.check_password_hash(user['password'], password):
			raise CustomError(error='LOGIN_PASSWORD_NOT_EQUAL',  msg='비밀번호가 일치하지 않습니다.', status=401)
		else:
			return jsonify(token=create_access_token(identity=id)), 200
	except CustomError as e:
		print(e)
		return e.to_response()

@app.route('/join', methods=['POST'])
def add_account_route():
	try:
		id = request.json['id']
		password = request.json['password']
		github_username = request.json['githubUsername']
		github_password = request.json['githubPassword']
		# if not exist_github_user(github_username):
		# 	raise CustomError(error = 'UNDEFINED_GITHUB_USERNAME', msg='존재하지 않은 깃허브 아이디입니다.', status=401)
		g.github_account_validate(github_username, github_password)

		encrypted_password = bcrypt.generate_password_hash(password)

		# 유저 db에 추가
		user = User(id, encrypted_password, github_username)
		db.add_user(user)

		return jsonify(success=True), 200
	except CustomError as e:
		print(e)
		return e.to_response()
	
# end - 계정 관련 코드
# ---------------------------------------------
@app.route('/get-leaked-repos', methods=['GET'])
@jwt_required
def get_leaked_repos():
	account_id = get_jwt_identity()
	repo_dicts = db.get_repositories_by_username(account_id)

	response = {}
	for repo_dict in repo_dicts:
		repo = db.repo_dict_to_obj(repo_dict)
		temp = db.get_recent_pull_num(repo)

		if temp['keyCount'] > 0:
			response[repo.fullname] = {
				'fullname': repo.fullname,
				'owner': repo.owner,
				'pull_request_url' : 'https://github.com/%s/pull/%s' % (repo.fullname, temp['pullNum']),
				'secret_key_count' : temp['keyCount'],
				'name' : repo.name
			}

	return jsonify(response), 200

@app.route('/get-secret-keys', methods=['POST'])
@jwt_required
def get_secret_keys():
	account_id = get_jwt_identity()
	repo_fullname = request.json['repo_fullname']

	repo = db.repo_dict_to_obj(db.get_repository(fullname = repo_fullname))

	if repo.owner != account_id:
		raise CustomError(error='UNAUTHORIZED', msg='접근할 수 없습니다.', status=401)

	secret_key_dicts = []

	for secret_key_dict in db.get_recent_secret_keys(repo=repo):
		secret_key_dicts.append(secret_key_dict)

	return jsonify(secret_key_dicts), 200



# 프로그램 종료시 실행
@atexit.register
def goodbye(): #인자 없어야 됨. 있으면 똥망
	print('core secret backend is dead')
	skf.stop()
	db.connection_close()