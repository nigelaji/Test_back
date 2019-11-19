# coding:utf-8
from flask import session, Response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps
import json
from tp_app.config import SECRET_KEY


def create_token(user, expire=600):     # 生成时效token，单位秒
    s = Serializer(secret_key=SECRET_KEY, expires_in=expire)
    token = s.dumps({'id': user.id})
    return token


def verify_token(token):    # token验证
    s = Serializer(secret_key=SECRET_KEY)    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    try:
        data = s.loads(token)   # 转换为字典
    except Exception:
        return None
    # user = User.query.get(data["id"])       # 拿到转换后的数据，根据模型类去数据库查询用户信息
    return data['id']   # 返回user_id


def require_token(func):    # 给需要登录的路由装上，就可以控制url必须登录才能访问了。
    @wraps(func)    # functools的wrap，它能保留原有函数的名称和docstring。
    def check_token(*args, **kwargs):
        # print('check_token ==>', session)
        if not session.get('token'):
            ret = {
                'code': -1,
                'msg': u'没有token，访问被拒绝！',
            }
            return Response(json.dumps(ret), status=401, mimetype='application/json')
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


def require_role_level(*role_level):  # 必须管理员角色等级验证
    def require(func):
        @wraps(func)
        def check_admin(*args, **kwargs):
            if session.get('current_user_role_id') in role_level:
                pass
            else:
                ret = {
                    'code': -3,
                    'msg': '辣鸡，你被拒绝了。哦哦好可怜哦！'
                }
                return Response(json.dumps(ret), status=403, mimetype='application/json')
            return func(*args, **kwargs)
        return check_admin
    return require
