# coding:utf-8
from flask import jsonify, request, redirect, session, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from tp_app import db
from . import user_blue
from tp_app.models import User, Role, Menu, user_role, role_menu, UserLogEvent
from tp_app.common.security import check_password
import time


def generate_token(key, expire=3600):   # 生成token
    return


def certify_token(key, token):  # 验证token
    
    return  True


# 用户邮箱注册
@user_blue.route('/register', methods=['POST'])
def register():
    """
    # 判断是否含有email、password1、password2、verification_code 参数，若没有则返回参数不全
    # 判断是否有invitationCode参数，若有则从redis数据库中获取邀请人，若获取不到则返回错误，参考REST
    # 获取phone参数，加密密码并将用户信息存入mysql数据，若成功则返回用户id，失败返回错误
    # 根据用户id生成邀请码，并存入redis数据库中
    # 判断是否有idfa参数，若有则在后台线程在mysql中修改用户来源（非必须同步操作，放后台即可）
    # 生成token
    """
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
        username = request.args.get('username')
        password = request.args.get('password')
        user = User.query.filter_by(username=username,password=password).first()
        if user:
            login_user(user)
            ret['data']['user'] = user
            return jsonify(ret)
        else:
            ret['code'] = 500
            ret['msg'] = "登录失败，用户名密码验证错误！"
            return jsonify(ret)


# 登出，GET
@user_blue.route('/logout')
@login_required     # 意思就是必须登录的用户才能请求的路由
def logout():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    x = logout_user()
    # UserLogEvent
    return jsonify(ret)


# 用户信息，GET查 POST增 PUT改 DELETE删
@user_blue.route('/user/profile', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def user_profile():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id)[0]
    if request.method == 'GET':
        
        return jsonify(user=user)
    if request.method == 'POST':
        return
    if request.method == 'PUT':
        return
    if request.method == 'DELETE':
        return
    return


# 密码修改POST
@user_blue.route('/user/password', methods=['POST'])
@login_required
def update_password():
    user_id = request.args.get('user_id')
    old_password = request.args.get('old_password')
    new_password1 = request.args.get('new_password1')
    new_password2 = request.args.get('new_password2')
    user = User.query.filter_by(id=user_id).first()
    if check_password(old_password, user.password):
        pass
    
    return
