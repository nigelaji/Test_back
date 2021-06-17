# coding:utf-8
from flask import request, session, Response, jsonify
from flask_login import current_user
from tp_app import db
from tp_app.views import user_blue
from tp_app.models import User, UserLogEvent
from tp_app.handler.http_handler import self_abort

from .auth import token_to_redis, require_token
import time
import json
from ...utils.encrypts.hash import StdHash


# from PIL import Image, ImageDraw


def check_password(password, pwd_hashed):  # 检查密码
    return StdHash.md5(password) == pwd_hashed


@user_blue.route('/register', methods=['POST'])
def register():
    """注册"""
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'POST':  # 邮箱注册
        email = request.json.get('email')
        password1 = request.json.get('password1')
        password2 = request.json.get('password2')
        verification_code = request.json.get('verification_code')
        if not (email and password1 and password2 and verification_code):
            self_abort(40101, '缺少必填信息')
        user = User.query.filter_by(email=email).first()
        if user:
            self_abort(40102, '邮箱已注册')
        if password1 != password2:
            self_abort(40103, '密码不一致')
        if verification_code != '1':
            self_abort(40104, '验证码错误')
        # 验证结束，创建用户基本信息
        user_default_name = 'TEST' + str(time.time())[0:10]
        user = User(username=user_default_name, password=password1, email=email)
        db.session.add(user)
        db.session.commit()
        ret['data'] = "用户新增成功！"
        return jsonify(ret)  # 注册成功，前端重定向到登录界面


@user_blue.route('/login', methods=['POST'])
def login():
    """登录"""
    ret = {
        'code': 200,
        'data': {}
    }
    if request.method == 'POST':
        if current_user.is_authenticated:
            pass
            # return redirect(url_for('index'))
        account = request.json.get('account') or request.form.get('account') or self_abort(40001, "账号必填")
        password = request.json.get('password') or request.form.get('password') or self_abort(40002, '密码必填')
        # request.form.get('...')     # 是从form表单中获取值的方式
        # request.args.get('...')     # 是从url链接后获取值的方式，一般是get方法用的
        # request.json.get('...')     # post请求，请求体是json串，请求头是这种类型的'Content-Type': "application/json",
        # request.values.get('...')   # 待定
        # request.data                # 二进制字节串
        user = User.query.filter((User.user_code == account) | (User.email == account)).first()
        if not user:
            self_abort(40003, '账号不存在')
        if user.locked == '0' or user.status == '0':
            self_abort(40004, '你的用户已被禁用或删除')
        if not check_password(password, user.password_hashlib):
            self_abort(40005, '密码验证失败')
        if not bool(user.roles):
            self_abort(40006, '此用户未授角色')

        flag, token = token_to_redis(user)  # 创建token
        if not flag:
            self_abort(40007, 'token 生成失败，请检查服务')

        ret['data'] = {
            "current_role_id": min([role.role_level for role in user.roles if role]),  # 权限最大的那个id
            "user_info": user.user_info,
            "user_roles": user.user_roles,
            "token": token
        }
        res = Response(json.dumps(ret), mimetype='application/json')
        UserLogEvent(user.id, request.remote_addr, 'login success')
        return res


@user_blue.route('/logout', methods=['GET'])
@require_token  # 意思就是必须登录的用户才能请求的路由,系统自带的装饰器
def logout():
    """登出"""
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    from tp_app.common.redisdb import RedisDB
    r = RedisDB()
    token = request.headers.get('token')
    r.session_del_token(token)
    u_id = token.split('-')[0]
    log_event = UserLogEvent(int(u_id), request.remote_addr, 'logout success')
    db.session.add(log_event)
    db.session.commit()
    ret['msg'] = '退出登录，清除token'
    return jsonify(ret)


# 用户信息，查
@user_blue.route('/profile', methods=['GET'])
@require_token
def user_profile():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'GET':
        user = User.query.filter_by(id=session['user_id']).first()
        ret['data'] = user.person_info
    return jsonify(ret)


# 密码修改POST
@user_blue.route('/password', methods=['POST'])
@require_token
def update_password():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'POST':
        old_password = request.json.get('old_password')
        new_password1 = request.json.get('new_password1')
        new_password2 = request.json.get('new_password2')
        user = User.query.filter_by(id=session['user_id']).first()
        if check_password(old_password, user.password):  # 先检查老密码是否正确
            if new_password1 == new_password2:  # 再检查两次新密码输入是否正确
                user.password = new_password1
                db.session.add(user)
                db.session.commit()
                ret['msg'] = '密码修改成功，重新登录获取token'
    return jsonify(ret)
