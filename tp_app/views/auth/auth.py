# coding:utf-8
from flask.app import session, Response, request
from functools import wraps
from tp_app.utils.encrypts.hash import StdHash
from tp_app.config import SECRET_KEY
from tp_app.common.redisdb import RedisDB
from tp_app.handler.http_handler import self_abort
import time
import pickle
import inspect
import json


def token_to_redis(user):
    try:
        timestamp = str(int(time.time()))
        u_id = user.id
        sha256 = StdHash.sha256(f"{u_id}#{timestamp}#{SECRET_KEY}")
        token = f"{u_id}-{sha256}"
        u_roles = pickle.dumps(user.user_roles)
        r = RedisDB()
        r.session_set_user_info(token, u_roles)
    except Exception as e:
        return False, e
    return True, token


def verify_token_from_redis(token):
    r = RedisDB()
    u_roles = r.session_get_user_info(token)
    if u_roles is None:
        return None
    return pickle.loads(u_roles)


def require_token(func):  # 给需要登录的路由装上，就可以控制url必须登录才能访问了。
    @wraps(func)  # functools的wrap，它能保留原有函数的名称和docstring。
    def check_token(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            self_abort(50001, '无权限访问')
        u_roles = verify_token_from_redis(token)
        if u_roles is None:
            self_abort(50002, 'token失效')
        return func(*args, **kwargs)

    return check_token


def require_role_level(*role_level):  # 必须管理员角色等级验证
    def require(func):
        @wraps(func)
        def check_admin(*args, **kwargs):
            if session.get('current_user_role_id') in role_level:
                pass
            else:
                ret = {
                    'code': -3,
                    'msg': u'权限不够，访问被拒绝！'
                }
                return Response(json.dumps(ret), status=403, mimetype='application/json')
            return func(*args, **kwargs)

        return check_admin

    return require


def token_for_members(cls):
    """给类的成员函数都加上require_token装饰器
    """
    for name, m in inspect.getmembers(cls, lambda m:  inspect.isfunction(m)):
        setattr(cls, name, require_token(m))
    return cls
