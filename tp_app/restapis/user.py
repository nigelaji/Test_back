# coding:utf-8
from flask_restful import Resource
# from flask_restful.reqparse import RequestParser
from .libs.selfreqparser import SelfRequestParser
from tp_app.models.authModels import User, Role, Menu, UserLogEvent
from tp_app import db
import traceback
from sqlalchemy.exc import IntegrityError

__all__ = [
    'UserListAPI', 'UserAPI', 'UserRoleAPI',
    'RoleListAPI', 'RoleAPI', 'RoleMenuAPI',
    'MenuListAPI', 'MenuAPI',
    'UserLogEventListAPI', 'UserLogEventAPI',
    'auth_resources'
]


class UserListAPI(Resource):

    def get(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        users = User.query.all()
        ret['data'] = [user.user_info for user in users]
        return ret

    def post(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('username', type=str, location='json')
        parse.add_argument('user_code', type=str, required=True, help='required', location='json')
        parse.add_argument('email', type=str, required=True, help='required', location='json')
        kwargs = parse.parse_args()
        kwargs.update({
            "password": "123456"  # 创建用户设置默认密码
        })
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
            ret['data'] = {
                "id": user.id
            }
        except IntegrityError as ie:
            ret.update({
                'code': 500,
                'msg': str(ie.orig)
            })
        except Exception:
            ret.update({
                'code': 500,
                'msg': traceback.format_exc()
            })
        return ret


class UserAPI(Resource):

    def get(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        user = User.query.filter_by(id=id).first()
        if user:
            ret['data'] = user.user_info
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def put(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('username', type=str, location='json')
        parse.add_argument('user_code', type=str, location='json')
        parse.add_argument('email', type=str, location='json')
        parse.add_argument('phone', type=str, location='json')
        parse.add_argument('remark', type=str, location='json')
        kwargs = parse.parse_args()
        user = User.query.filter_by(id=id).first()
        if user:
            for k, v in kwargs.items():
                if v is None:
                    break
                else:
                    exist = User.query.filter_by({k, v}).first()
                    if exist:
                        ret.update({
                            'code': 405,
                            'msg': f'{k}已被使用'
                        })
                        return ret
                setattr(user, k, v)
            db.session.add(user)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def delete(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret


class UserRoleAPI(Resource):

    def get(self):
        """获取账户的角色信息列表"""
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('id', type=str, required=True, help='required', location='args')
        kwargs = parse.parse_args()
        user = User.query.filter_by(id=kwargs['id']).first()
        if user:
            ret['data'] = user.user_roles
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def put(self):
        """用户绑定或解绑角色"""
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('user_id', type=str, required=True, help='required', location='json')
        parse.add_argument('role_ids', type=tuple, required=True, help='required', location='json')
        kwargs = parse.parse_args()
        try:
            user = User.query.filter_by(id=kwargs.get('user_id')).first()
            roles = Role.query.filter(Role.id.in_(kwargs.get('role_ids'))).all()
            user.roles = roles
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            ret.update({
                'code': 500,
                'msg': traceback.format_exc()
            })
        return ret


class RoleListAPI(Resource):
    def get(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        roles = Role.query.all()
        ret['data'] = [role.role_info for role in roles]
        return ret

    def post(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('role_name', type=str, required=True, help='required', location='json')
        parse.add_argument('role_level', type=str, required=True, help='required', location='json')
        parse.add_argument('introduction', type=str, location='json')
        kwargs = parse.parse_args()
        try:
            role = Role(**kwargs)
            db.session.add(role)
            db.session.commit()
            ret['data'] = role.role_info
        except Exception:
            ret.update({
                'code': 500,
                'msg': traceback.format_exc()
            })
        return ret


class RoleAPI(Resource):
    def get(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        role = Role.query.filter_by(id=id).first()
        if role:
            ret['data'] = role.role_info
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def put(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('role_name', type=str, location='json')
        parse.add_argument('role_level', type=str, location='json')
        # parse.add_argument('password', type=str, location='json')
        parse.add_argument('introduction', type=str, location='json')
        parse.add_argument('create_user_id', type=str, location='json')
        parse.add_argument('menus', type=str, location='json')
        kwargs = parse.parse_args()
        role = Role.query.filter_by(id=id).first()
        if role:
            for k, v in kwargs.items():
                if v is None:
                    break
                setattr(role, k, v)
            db.session.add(role)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def delete(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        role = Role.query.filter_by(id=id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': "资源不存在"
            })
        return ret


class RoleMenuAPI(Resource):
    def put(self):
        """单个角色绑定多个菜单"""
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('role_id', type=str, location='json')
        parse.add_argument('menus_ids', type=list, location='json')
        kwargs = parse.parse_args()


class MenuListAPI(Resource):

    def get(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        menus = Menu.query.all()
        ret['data'] = [menu.menu_info for menu in menus]
        return ret

    def post(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('menu_name', type=str, required=True, help='required', location='json')
        parse.add_argument('menu_url', type=str, required=True, help='required', location='json')
        parse.add_argument('icon_class', type=str, location='json')
        parse.add_argument('parent_id', type=str, location='json')
        kwargs = parse.parse_args()
        try:
            menu = Menu(**kwargs)
            db.session.add(menu)
            db.session.commit()
            ret['data'] = menu.role_info
        except Exception:
            ret.update({
                'code': 500,
                'msg': traceback.format_exc()
            })
        return ret


class MenuAPI(Resource):
    def get(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            ret['data'] = menu.menu_info
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def put(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        parse = SelfRequestParser()
        parse.add_argument('menu_name', type=str, location='json')
        parse.add_argument('menu_url', type=str, location='json')
        parse.add_argument('icon_class', type=str, location='json')
        parse.add_argument('parent_id', type=str, location='json')
        kwargs = parse.parse_args()
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            for k, v in kwargs.items():
                if v is None:
                    break
                setattr(menu, k, v)
            db.session.add(menu)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret

    def delete(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            db.session.delete(menu)
            db.session.commit()
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret


class UserLogEventListAPI(Resource):
    def get(self):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        log_events = UserLogEvent.query.all()
        ret['data'] = [log_event.log_info for log_event in log_events]
        return ret


class UserLogEventAPI(Resource):
    def get(self, id):
        ret = {
            "code": 200,
            "data": {},
            "msg": "ok"
        }
        log_event = UserLogEvent.query.filter_by(id=id).first()
        if log_event:
            ret['data'] = log_event.log_info
        else:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
        return ret


auth_resources = [
    {
        'resource': UserListAPI,
        'urls': '/users'
    },
    {
        'resource': UserAPI,
        'urls': '/users/<int:id>'
    },
    {
        'resource': UserRoleAPI,
        'urls': '/users/roles'
    },
    {
        'resource': RoleListAPI,
        'urls': '/roles'
    },
    {
        'resource': RoleAPI,
        'urls': '/roles/<int:id>'
    },
    {
        'resource': RoleMenuAPI,
        'urls': '/role/menus'
    },
    {
        'resource': MenuListAPI,
        'urls': '/menus'
    },
    {
        'resource': MenuAPI,
        'urls': '/menus/<int:id>'
    },
    {
        'resource': UserLogEventListAPI,
        'urls': '/events'
    },
    {
        'resource': UserLogEventAPI,
        'urls': '/events/<int:id>'
    }
]
