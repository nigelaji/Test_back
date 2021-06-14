# coding:utf-8
# from flask_restful import Resource
# from flask_restful.reqparse import RequestParser
from .libs.selfreqparser import SelfRequestParser
from .libs.selfresource import SelfResource
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


class UserListAPI(SelfResource):

    def get(self):
        users = User.query.all()
        self.ret['data'] = [user.user_info for user in users]
        return self.ret

    def post(self):
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
            self.ret['data'] = {
                "id": user.id
            }
            self.ret['msg'] = '创建成功'
        except IntegrityError as ie:
            self.ret['msg'] = str(ie.orig)
        except Exception:
            self.ret['msg'] = traceback.format_exc()
        return self.ret


class UserAPI(SelfResource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            self.ret['data'] = user.user_info
        else:
            self.ret['msg'] = '用户不存在'
        return self.ret

    def put(self, id):
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
                        self.ret['msg'] = f'{k}已被使用'
                        return self.ret
                setattr(user, k, v)
            db.session.add(user)
            db.session.commit()
            self.ret['msg'] = "修改成功"
        else:
            self.ret['msg'] = '用户不存在'
        return self.ret

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            self.ret['msg'] = '删除成功'
        return self.ret


class UserRoleAPI(SelfResource):

    def get(self):
        """获取账户的角色信息列表"""
        parse = SelfRequestParser()
        parse.add_argument('id', type=str, required=True, help='required', location='args')
        kwargs = parse.parse_args()
        user = User.query.filter_by(id=kwargs['id']).first()
        self.ret['data'] = user.user_roles
        return self.ret

    def put(self):
        """用户绑定或解绑角色"""
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
            self.ret['msg'] = e
        return self.ret


class RoleListAPI(SelfResource):
    def get(self):
        roles = Role.query.all()
        self.ret['data'] = [role.role_info for role in roles]
        return self.ret

    def post(self):
        parse = SelfRequestParser()
        parse.add_argument('role_name', type=str, required=True, help='required', location='json')
        parse.add_argument('role_level', type=str, required=True, help='required', location='json')
        parse.add_argument('introduction', type=str, location='json')
        kwargs = parse.parse_args()
        try:
            role = Role(**kwargs)
            db.session.add(role)
            db.session.commit()
            self.ret['data'] = role.role_info
        except Exception:
            self.ret['msg'] = traceback.format_exc()
        return self.ret


class RoleAPI(SelfResource):
    def get(self, id):
        role = Role.query.filter_by(id=id).first()
        if role:
            self.ret['data'] = role.role_info
        else:
            self.ret['msg'] = '角色不存在'
        return self.ret

    def put(self, id):
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
            self.ret['msg'] = "修改成功"
        return self.ret

    def delete(self, id):
        role = Role.query.filter_by(id=id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            self.ret['msg'] = '删除成功'
        return self.ret


class RoleMenuAPI(SelfResource):
    def put(self):
        """单个角色绑定多个菜单"""
        parse = SelfRequestParser()
        parse.add_argument('role_id', type=str, location='json')
        parse.add_argument('menus_ids', type=list, location='json')
        kwargs = parse.parse_args()


class MenuListAPI(SelfResource):

    def get(self):
        menus = Menu.query.all()
        self.ret['data'] = [menu.menu_info for menu in menus]
        return self.ret

    def post(self):
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
            self.ret['data'] = menu.role_info
        except Exception:
            self.ret['msg'] = traceback.format_exc()
        return self.ret


class MenuAPI(SelfResource):
    def get(self, id):
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            self.ret['data'] = menu.menu_info
        else:
            self.ret['msg'] = '菜单不存在'
        return self.ret

    def put(self, id):
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
            self.ret['msg'] = "修改成功"
        return self.ret

    def delete(self, id):
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            db.session.delete(menu)
            db.session.commit()
            self.ret['msg'] = '删除成功'
        return self.ret


class UserLogEventListAPI(SelfResource):
    def get(self):
        log_events = UserLogEvent.query.all()
        self.ret['data'] = [log_event.log_info for log_event in log_events]
        return self.ret


class UserLogEventAPI(SelfResource):
    def get(self, id):
        log_event = UserLogEvent.query.filter_by(id=id).first()
        if log_event:
            self.ret['data'] = log_event.log_info
        else:
            self.ret['msg'] = '事件不存在'
        return self.ret


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
