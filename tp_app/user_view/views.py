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
            return Response("没有token，访问被拒绝！")
        else:
            user = verify_token(session['token'])
            if not user:
                return redirect('/login', Response('token失效，请重新登录！'))
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
        username = request.args.get('username')
        password = request.args.get('password')
        user = User.query.filter_by(username=username,password=password).first()
        if user:
            login_user(user)
            ret['data']['user'] = user
            token = create_token(user)  # 创建token
            session['token'] = token    # session中加token，后续请求中session中带token的才可以请求需要登录的url
            return jsonify(ret)
        else:
            ret['code'] = 500
            ret['msg'] = "登录失败，用户名密码验证错误！"
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
@user_blue.route('/user/profile', methods=['POST'])
@require_token
def user_profile():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    user_id = request.json.get('user_id')
    user = User.query.filter_by(user_id=user_id)[0]
    if request.method == 'POST':
        if not user:
            ret['msg'] = '用户不存在！'
            return jsonify(ret)
        ret['data'] = {
            'username': user.username,
            'user_code': user.user_code,
            'email': user.email,
            'phone': user.phone,
            'remark': user.remark,
        }
    return jsonify(ret)


# 密码修改POST
@user_blue.route('/user/password', methods=['POST'])
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
