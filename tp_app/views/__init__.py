# coding:utf-8
from flask import Blueprint

user_blue = Blueprint('user', __name__)
article_blue = Blueprint('article', __name__)

from tp_app.views.user import views
from tp_app.views.user import auth

import json
from flask import make_response, jsonify, Response, session, request
from tp_app import app, db
from tp_app.common.utils import times_count
from tp_app.handler.logger_handler import logger
import time


@app.route('/')
def index():
    print(session)
    return 'hello world'


@app.route('/get_verification_code')  # 验证码获取接口
def get_verification_code():
    ret = {
        'code': 200,
        'msg': '获取验证码',
        'data': {}
    }
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/init_data')  # 初始化数据库数据
def init_data():
    ret = {
        'code': 200,
        'msg': '初始化数据',
        'data': {}
    }
    return jsonify(ret)


# 三种方式返回Content-Type: application/json类型数据
@app.route('/test1')  # jsonify方式
def test1():
    ret = {
        'code': 200,
        'msg': 'test1',
        'data': {}
    }
    return jsonify(ret)


@app.route('/test2')  # Response类构造方式
def test2():
    ret = {
        'code': 200,
        'msg': 'test2',
        'data': {}
    }
    return Response(json.dumps(ret), mimetype='application/json')


@app.route('/test3')  # make_response方法构造
def test3():
    ret = {
        'code': 200,
        'msg': 'test3',
        'data': {}
    }
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/init_count')
@times_count
def init_count():
    # print(dir(request))
    print(request.host)
    return jsonify({
        "code": 200,
        "message": "ok",
    })


@app.route('/eventRcv', methods=['POST'])
@times_count
def eventRcv():
    logger.info(request.json or '空')
    # http://10.9.82.15:5000/eventRcv # http://122.112.173.59:5000/eventRcv
    # print(request.remote_addr)
    # print(request.json.get('data').get('userId'))
    # if request.json.get('data').get('userId') == 125496:
    #     print(request.remote_addr, request.json)
    # print(request.remote_addr, request.json)
    return jsonify({
        "code": 200,
        "message": "success",
        "desc": "",
        "data": {}
    })
