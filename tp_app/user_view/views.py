# coding:utf-8
from flask import jsonify, request, redirect, session, Response
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from tp_app import db, app
from . import user_blue
from tp_app.models import User, Role, Menu, user_role, role_menu, UserLogEvent
from tp_app.common.security import check_password
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps
import json


def create_token(user):     # 生成时效token
    s = Serializer('secret-key', expires_in=60)
    token = s.dumps({'id': user.id}).decode("ascii")
    return token


def verify_token(token):    # token验证
    s = Serializer(app.config["SECRET_KEY"])    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    try:
        data = s.loads(token)   # 转换为字典
    except Exception:
        return None
    user = User.query.get(data["id"])       # 拿到转换后的数据，根据模型类去数据库查询用户信息
    return user


def require_token(func):    # 给需要登录的路由装上，就可以控制url必须登录才能访问了。
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'token' not in session:
            ret = {
                'code': -1,
                'msg': u'没有token，访问被拒绝！',
            }
            return Response(json.dumps(ret), mimetype='application/json')
        else:
            user = verify_token(session['token'])
            if not user:
                ret = {
                    'code': -2,
                    'msg': u'token失效，请重新登录！',
                }
                return Response(json.dumps(ret), mimetype='application/json')
        return func(*args, **kwargs)
    return check_token


# 用户邮箱注册
@user_blue.route('/register', methods=['POST'])
def register():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'POST':    # 邮箱注册
        # user = User.query.filter_by(email=request.POST.get('')).first()
        email = request.json.get('email')
        password1 = request.args.get('password1')
        password2 = request.args.get('password2')
        verification_code = request.args.get('verification_code')
        # 开始验证注册信息
        if email and password1 and password2 and verification_code:
            ret['msg'] = "缺少必填信息！"
            return jsonify(ret)
        user = User.query.filter_by(email=email).first()
        if user:
            ret['msg'] = "邮箱已注册！"
            return jsonify(ret)
        if password1 != password2:
            ret['msg'] = "密码不一致！"
            return jsonify(ret)
        if verification_code != '1':
            ret['msg'] = "验证码错误！"
            return jsonify(ret)
        # 验证结束，创建用户基本信息
        user_default_name = 'TEST'+str(time.time())[0:10]
        user = User(username=user_default_name, password=password1, email=email)
        db.session.add(user)
        db.session.commit()
        print("用户新增成功！")
        return redirect('/user/profile/')  # 注册成功，重定向到个人profile页面，可修改信息


# 用户登录
@user_blue.route('/login', methods=['POST'])
def login():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'POST':
        # print(request.values)
        user_code = request.values.get('user_code') or 'admin'    # args只获取地址栏中参数
        password = request.values.get('password') or '123456'
        # print(user_code, password)
        user = User.query.filter_by(user_code=user_code).first()
        if not check_password(password, user.password_hashlib):
            ret['msg'] = '密码验证失败！'
            return jsonify(ret)
        if user:
            login_user(user)
            ret['data'] = user.serialize
            token = create_token(user)  # 创建token
            session['token'] = token    # session中加token，后续请求中session中带token的才可以请求需要登录的url
            print(token)
            return jsonify(ret)


# 登出，GET
@user_blue.route('/logout')
@login_required     # 意思就是必须登录的用户才能请求的路由,系统自带的装饰器
def logout():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    x = logout_user()
    # UserLogEvent
    return jsonify(ret)


# 用户信息，查
@user_blue.route('/profile', methods=['POST'])
@require_token
def user_profile():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    user_id = request.json.get('user_id') or 1
    user = User.query.filter_by(user_id=user_id)[0]
    if request.method == 'POST':
        if not user:
            ret['msg'] = '用户不存在！'
            return jsonify(ret)
        ret['data'] = user.serialize
    return jsonify(ret)


# 密码修改POST
@user_blue.route('/password', methods=['POST'])
@require_token
def update_password():
    user_id = request.args.get('user_id')
    old_password = request.args.get('old_password')
    new_password1 = request.args.get('new_password1')
    new_password2 = request.args.get('new_password2')
    user = User.query.filter_by(id=user_id).first()
    if check_password(old_password, user.password):
        pass
    
    return


# ---------------角色增删改查，角色关联菜单------------------
@user_blue.route('/role/add', methods=['POST'])
@require_token
def add_role():
    return


@user_blue.route('/role/delete', methods=['POST'])
@require_token
def delete_role():
    return


@user_blue.route('/role/update', methods=['POST'])
@require_token
def update_role():
    return


@user_blue.route('/role/list', methods=['GET'])
@require_token
def role_list():
    return


@user_blue.route('/role/authorize_menu', methods=['POST'])  # 授权菜单
@require_token
def authorize_menu():
    return


# ----------------菜单增删改查----------------------
@user_blue.route('/menu/add', methods=['POST'])     # 建菜单目录和菜单
@require_token
def add_menu():
    #
    return


@user_blue.route('/menu/delete', methods=['POST'])
@require_token
def delete_menu():
    return


@user_blue.route('/menu/update', methods=['POST'])
@require_token
def update_menu():
    return


@user_blue.route('/menu/list', methods=['GET'])
@require_token
def menu_list():
    return

