# coding:utf-8
import json
from flask import make_response, jsonify, Response
from tp_app import app


@app.route('/')
def index():
	return 'hello world'


@app.route('/get_verification_code')		# 验证码获取接口
def get_verification_code():
	ret = {
		'code': 200,
		'msg': '获取验证码',
		'data': {}
	}
	response = make_response(json.dumps(ret))
	response.headers['Content-Type'] = 'application/json'
	return response


@app.route('/init_data')		# 初始化数据库数据
def init_data():
	ret = {
		'code': 200,
		'msg': '初始化数据',
		'data': {}
	}
	return jsonify(ret)


# 三种方式返回Content-Type: application/json类型数据
@app.route('/test1')		# jsonify方式
def test1():
	ret = {
		'code': 200,
		'msg': 'test1',
		'data': {}
	}
	return jsonify(ret)


@app.route('/test2')		# Response类构造方式
def test2():
	ret = {
		'code': 200,
		'msg': 'test2',
		'data': {}
	}
	return Response(json.dumps(ret), mimetype='application/json')


@app.route('/test3')		# make_response方法构造
def test3():
	ret = {
		'code': 200,
		'msg': 'test3',
		'data': {}
	}
	response = make_response(json.dumps(ret))
	response.headers['Content-Type'] = 'application/json'
	return response

