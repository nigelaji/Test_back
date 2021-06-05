# coding:utf-8
from flask import jsonify, request, session, Response, abort, g
from tp_app import db, app
from tp_app.views import user_blue
from tp_app.models import User, Role, Menu, user_role, role_menu, UserLogEvent
from tp_app.common.security import check_password
from .auth import create_token, require_token, require_role_level
import time
import json
import traceback
# from PIL import Image, ImageDraw


# 用户邮箱注册
from tp_app.models.articleModels import Article


@user_blue.route('/register', methods=['POST'])
def register():
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
        user_default_name = 'TEST' + str(time.time())[0:10]
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
        user_code = request.json.get('user_code')  # 请求中的json一定要是标准格式的，引号要双引号
        password = request.json.get('password')
        # request.form.get('...')     # 是从form表单中获取值的方式
        # request.args.get('...')     # 是从url链接后获取值的方式，一般是get方法用的
        # request.json.get('...')     # post请求，请求体是json串，请求头是这种类型的'Content-Type': "application/json",
        # request.values.get('...')   # 待定
        # request.data                # 二进制字节串
        user = User.query.filter_by(user_code=user_code).first()
        if user:
            if user.locked == '0' or user.status == '0':
                ret['msg'] = '你的用户已被禁用或删除'
                return jsonify(ret)
            if not check_password(password, user.password_hashlib):
                ret['msg'] = '密码验证失败！'
                return jsonify(ret)
            # print(session)  # 如果这个也打印出来键值，一定是上次请求遗留下来的
            # login_user(user)    # 这个方法会给session中自动添加user_id,_fresh,_id三个键值
            # ret['data'] = user.serialize
            token = create_token(user)  # 创建token
            session['user_id'] = user.id  # session中只能存储可序列化的值，包括二层、三层..
            # session['current_user_role_id'] = [role.role_level for role in user.roles if role]
            session['current_user_role_id'] = min([role.role_level for role in user.roles if role])
            role_menu_serialize = Role.query.get(session['current_user_role_id']).serialize
            session['token'] = token  # session中加token，后续请求中session中带token的才可以请求需要登录的url
            ret['data'] = user.serialize
            ret['data']['current_role_menus'] = role_menu_serialize
            res = Response(json.dumps(ret), mimetype='application/json')
            res.set_cookie('token', token)  # 之后前端拿着这个令牌就可以为所欲为了
            # print('login ==>', session)
            # 记录登录事件 UserLogEvent
            log_event = UserLogEvent(user.id, request.remote_addr, 'login success')
            db.session.add(log_event)
            db.session.commit()
            return res
        else:
            abort(404)


# 登出，GET
@user_blue.route('/logout', methods=['POST'])
@require_token  # 意思就是必须登录的用户才能请求的路由,系统自带的装饰器
def logout():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    session.pop('token')
    # UserLogEvent
    log_event = UserLogEvent(session['user_id'], request.remote_addr, 'logout success')
    db.session.add(log_event)
    db.session.commit()
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


# ---------获取用户的一些东西-------
@user_blue.route('/roles_menus', methods=['POST'])
@require_token
def user_roles_menus():
    # 获取用户角色和菜单
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        user = User.query.filter_by(id=session['user_id']).first()
        ret['data'] = [role.serialize for role in user.roles if role]
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)


# ---------------角色增删改查，角色关联菜单------------------
@user_blue.route('/role/add', methods=['POST'])
@require_role_level(1, 2)
@require_token
def add_role():  # 新增角色
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        role = Role(**request.json, create_user_id=session['user_id'])
        db.session.add(role)
        db.session.commit()
        ret['msg'] = "角色新增成功"
    except TypeError as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)


@user_blue.route('/role/update', methods=['POST'])
@require_role_level(1, 2)
@require_token
def update_role():  # 适用软删除和更新
    # 角色只能超级管理员更改
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        role_id = request.json.pop('role_id')  # 前端请求的role_id
        sess_role = Role.query.filter_by(id=session['current_user_role_id']).first()  # session中存储的role_id
        role = None
        if sess_role.role_level == 1:
            # 最高级角色权限的可以改所有角色
            role = Role.query.filter_by(id=int(role_id)).first()
        elif sess_role.role_level == 2:
            # 普通管理员只能改自己建的
            role = Role.query.filter_by(id=int(role_id), create_user_id=session['user_id']).first()
        else:
            abort(404)
        if role:
            role = Role.query.filter_by(id=int(role_id)).first()
            for k, v in request.json.items():
                if k in role.__dict__:
                    role.__setattr__(k, v)  # 不能role.__dict__[k] = v这种方式改，改不成功的
        else:
            ret['code'] = -1
            ret['msg'] = "别人的角色你改啥？很牛逼？"
            return jsonify(ret)
        db.session.add(role)
        db.session.commit()
        ret['msg'] = "角色更新或删除成功"
    except Exception:
        ret['msg'] = traceback.format_exc()
    return jsonify(ret)


@user_blue.route('/role/list', methods=['GET', 'POST'])
@require_role_level(1, 2)
@require_token
def role_list():
    # 超级管理员可以看到所有的，管理员只能看到自己建的
    if request.method == 'POST':
        pageSize = request.json.get('pageSize') or 1
        pageNum = request.json.get('pageNum') or 10
        if session['current_user_role_id'] == 1:
            pagination = Role.query.filter_by(status='1').paginate(pageSize, per_page=pageNum, error_out=False)
        else:
            pagination = Role.query.filter_by(status='1', create_user_id=session['user_id']).paginate(pageSize,
                                                                                                      per_page=pageNum,
                                                                                                      error_out=False)
        roles = pagination.items
        res = []
        for role in roles:
            res.append(role.role_info)
        return jsonify(res)
    else:
        abort(405)  # 405 客户端请求中的方法被禁止


@user_blue.route('/role/authorize_user', methods=['POST'])  # 角色授权用户
@require_role_level(1, 2)
@require_token
def authorize_role():
    # 只有管理员能授权用户角色，且不能授权管理员角色和超级管理员角色
    # 可以对用户授权多个角色
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    role_id_list = request.json.get('role_id_list')
    target_user = User.query.filter_by().first()
    target_role = Role.query.filter_by(id in role_id_list)
    target_user.roles = target_role
    db.session.add(target_user)
    db.session.commit()
    return


# ----------------菜单增删改查，菜单只有超级管理员可更改----------------------
@user_blue.route('/menu/add', methods=['POST'])  # 建菜单目录和菜单
@require_role_level(1)
@require_token
def add_menu():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        menu = Menu(**request.json)
        db.session.add(menu)
        db.session.commit()
        ret['msg'] = "菜单新增成功"
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)


@user_blue.route('/menu/update', methods=['POST'])
@require_role_level(1)
@require_token
def update_menu():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        menu_id = request.json.pop('menu_id')
        menu = Menu.query.filter_by(id=int(menu_id)).first()
        for k, v in request.json.items():
            if k in menu.__dict__:
                menu.__setattr__(k, v)  # 不能menu.__dict__[k] = v这种方式改，改不成功的
        db.session.add(menu)
        db.session.commit()
        ret['msg'] = "菜单更新或删除成功"
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)


@user_blue.route('/menu/list', methods=['GET'])  # 菜单列表
@require_role_level(1)
@require_token
def menu_list():
    pageSize = request.json.get('pageSize') or 1
    pageNum = request.json.get('pageNum') or 10
    pagination = Menu.query.filter_by(status='1').paginate(pageSize, per_page=pageNum, error_out=False)
    menus = pagination.items
    res = []
    for menu in menus:
        res.append(menu.serialize)
    return jsonify(res)


@user_blue.route('/menu/authorize_role', methods=['POST'])  # 授权角色菜单
@require_role_level(1)
@require_token
def authorize_menu():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        role_id = request.json.get('role_id')
        menu_id_list = request.json.get('menu_id_list')
        target_role = Role.query.filter_by(id=int(role_id)).first()
        target_menu = Menu.query.filter_by(id in menu_id_list)
        target_role.menus = target_menu
        db.session.add(target_role)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)


@user_blue.route('/article', methods=['GET'])  # 获取文章内容
# @require_role_level(1)
# @require_token
def get_article():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        article_id = request.args.get('id')
        # article_id = request.json.get('id')
        article = Article.query.filter_by(id=article_id).first()
        ret['data'] = {
            'title': article.title,
            'content': article.content
        }
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)
