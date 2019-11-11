# coding:utf-8
from flask import jsonify, request, redirect, session, Response, abort
# from flask_login import login_user, logout_user, current_user, require_token
from tp_app import db, app
from . import user_blue
from tp_app.models import User, Role, Menu, user_role, role_menu, UserLogEvent
from tp_app.common.security import check_password
from tp_app.config import SECRET_KEY
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps
import json
import traceback


def create_token(user, expire=3600):     # 生成时效token
    s = Serializer(secret_key=SECRET_KEY, expires_in=expire)
    token = s.dumps({'id': user.id})
    return token


def verify_token(token):    # token验证
    s = Serializer(secret_key=SECRET_KEY)    # 参数为私有秘钥，跟上面方法的秘钥保持一致
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
        email = request.json.get('email')
        password1 = request.json.get('password1')
        password2 = request.json.get('password2')
        verification_code = request.json.get('verification_code')
        print(email, password1, password2, verification_code)
        # 开始验证注册信息
        if not (email and password1 and password2 and verification_code):
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
        ret['data'] = "用户新增成功！"
        return jsonify(ret)  # 注册成功，前端可重定向到个人profile页面，可修改信息


# 用户登录
@user_blue.route('/login', methods=['POST'])
def login():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    if request.method == 'POST':
        # print(request.values, request.json, request.args, request.form, request.data)
        user_code = request.json.get('user_code')    # 请求中的json一定要是标准格式的，引号要双引号
        password = request.json.get('password')
        # request.form.get('...')     # 是从form表单中获取值的方式
        # request.args.get('...')     # 是从url链接后获取值的方式，一般是get方法用的
        # request.json.get('...')     # post请求，请求体是json串，请求头是这种类型的'Content-Type': "application/json",
        # request.values.get('...')   # 待定
        # request.data                # 二进制字节串
        user = User.query.filter_by(user_code=user_code).first()
        if not check_password(password, user.password_hashlib):
            ret['msg'] = '密码验证失败！'
            return jsonify(ret)
        if user:
            # print(session)  # 如果这个也打印出来键值，一定是上次请求遗留下来的
            # login_user(user)    # 这个方法会给session中自动添加user_id,_fresh,_id三个键值
            # ret['data'] = user.serialize
            token = create_token(user)  # 创建token
            session['user'] = user
            session['token'] = token    # session中加token，后续请求中session中带token的才可以请求需要登录的url
            ret['data'] = user.serialize
            res = Response(json.dumps(ret), mimetype='application/json')
            res.set_cookie('token', token)  # 之后前端拿着这个令牌就可以为所欲为了
            # print(session)
            return res


# 登出，GET
@user_blue.route('/logout', methods=['POST'])
@require_token     # 意思就是必须登录的用户才能请求的路由,系统自带的装饰器
def logout():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    session.pop('token')
    # UserLogEvent
    ret['msg'] = '退出登录，清除token'
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
    if request.method == 'POST':
        user = verify_token(session['token'])
        user = User.query.filter_by(id=int(user.id)).first()
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
        if check_password(old_password, user.password):     # 先检查老密码是否正确
            if new_password1 == new_password2:              # 再检查两次新密码输入是否正确
                user.password = new_password1
                db.session.add(user)
                db.session.commit()
                ret['msg'] = '密码修改成功，重新登录获取token'
    return jsonify(ret)


# ---------获取用户的一些东西-------
@user_blue.route('/user/roles', methods=['POST'])
@require_token
def user_menu():
    # 获取用户角色
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        pass
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)


@user_blue.route('/user/menus', methods=['POST'])
@require_token
def user_menu():
    # 用户通过角色获取菜单，用户切换角色时的菜单
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        pass
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)



# ---------------角色增删改查，角色关联菜单------------------
@user_blue.route('/role/add', methods=['POST'])
@require_token
def add_role():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        role = Role(**request.json)
        db.session.add(role)
        db.session.commit()
        ret['msg'] = "角色新增成功"
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)


@user_blue.route('/role/update', methods=['POST'])
@require_token
def update_role():      # 适用软删除和更新
    # 角色只能超级管理员更改
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        role_id = request.json.get('role_id')
        role = Role.query.filter_by(id=int(role_id)).first()
        for k, v in request.json.items():
            if k in role.__dict__:
                role.__dict__['k'] = v
        db.session.add(role)
        db.session.commit()
        ret['msg'] = "角色更新成功"
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)


@user_blue.route('/role/list', methods=['GET'])
@require_token
def role_list():
    # 角色列表只能管理员查看
    
    pageSize = request.args.get('pageSize', 1, type=int)
    pageNum = request.args.get('pageNum', 10, type=int)
    pagination = Role.query.paginate(pageSize, per_page=pageNum, error_out=False)
    roles = pagination.items
    res = []
    for role in roles:
        temp_role = {'id': role.id, 'name': role.role_name}
        res.append(temp_role)
    return jsonify(res)


@user_blue.route('/role/authorize_user', methods=['POST'])  # 授权用户角色
@require_token
def authorize_role():
    # 只有管理员能授权用户角色，且不能授权管理员角色，普通管理员不能授权超级管理员角色
    return


# ----------------菜单增删改查，菜单只有超级管理员可更改----------------------
@user_blue.route('/menu/add', methods=['POST'])     # 建菜单目录和菜单
@require_token
def add_menu():
    #
    return


@user_blue.route('/menu/update', methods=['POST'])
@require_token
def update_menu():
    return


@user_blue.route('/menu/list', methods=['GET'])
@require_token
def menu_list():
    # 这是查看菜单列表的接口
    return


@user_blue.route('/menu/authorize_role', methods=['POST'])  # 授权角色菜单
@require_token
def authorize_menu():
    return
