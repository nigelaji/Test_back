# coding:utf-8
from flask_restful import Resource, reqparse
from tp_app.models.authModels import User, Role, Menu, UserLogEvent
from tp_app import db
import traceback

ret = {
    'code': 200,
    'data': {},
    'msg': '',

}


class UserListAPI(Resource):
    def get(self):
        users = User.query.all()
        ret['data'] = [user.user_info for user in users]
        return ret

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, required=True, help='required', location='json')
        parse.add_argument('user_code', type=str, required=True, help='required', location='json')
        parse.add_argument('password', type=str, required=True, help='required', location='json')
        parse.add_argument('email', type=str, required=True, help='required', location='json')
        kwargs = parse.parse_args()
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
            ret['data'] = user.user_info
        except Exception:
            ret['msg'] = traceback.format_exc()
        return ret


class UserAPI(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            ret['data'] = user.user_info
        else:
            ret['msg'] = '用户不存在'
        return ret

    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, location='json')
        parse.add_argument('user_code', type=str, location='json')
        # parse.add_argument('password', type=str, location='json')
        parse.add_argument('email', type=str, location='json')
        parse.add_argument('phone', type=str, location='json')
        parse.add_argument('locked', type=str, location='json')
        parse.add_argument('remark', type=str, location='json')
        kwargs = parse.parse_args()
        user = User.query.filter_by(id=id).first()
        if user:
            for k, v in kwargs.items():
                if v is None:
                    break
                setattr(user, k, v)
            db.session.add(user)
            db.session.commit()
            ret['msg'] = "修改成功"
        return ret

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            ret['msg'] = '删除成功'
        return ret


class RoleListAPI(Resource):
    def get(self):
        roles = Role.query.all()
        ret['data'] = [role.role_info for role in roles]
        return ret

    def post(self):
        parse = reqparse.RequestParser()
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
            ret['msg'] = traceback.format_exc()
        return ret


class RoleAPI(Resource):
    def get(self, id):
        role = Role.query.filter_by(id=id).first()
        if role:
            ret['data'] = role.user_info
        else:
            ret['msg'] = '角色不存在'
        return ret

    def put(self, id):
        parse = reqparse.RequestParser()
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
            ret['msg'] = "修改成功"
        return ret

    def delete(self, id):
        role = Role.query.filter_by(id=id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            ret['msg'] = '删除成功'
        return ret


class MenuListAPI(Resource):

    def get(self):
        menus = Menu.query.all()
        ret['data'] = [menu.menu_info for menu in menus]
        return ret

    def post(self):
        parse = reqparse.RequestParser()
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
            ret['msg'] = traceback.format_exc()
        return ret


class MenuAPI(Resource):
    def get(self, id):
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            ret['data'] = menu.user_info
        else:
            ret['msg'] = '菜单不存在'
        return ret

    def put(self, id):
        parse = reqparse.RequestParser()
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
            ret['msg'] = "修改成功"
        return ret

    def delete(self, id):
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            db.session.delete(menu)
            db.session.commit()
            ret['msg'] = '删除成功'
        return ret


class UserLogEventListAPI(Resource):
    def get(self):
        log_events = UserLogEvent.query.all()
        ret['data'] = [ log_event.log_info for log_event in log_events ]
        return ret


class UserLogEventAPI(Resource):
    def get(self, id):
        log_event = UserLogEvent.query.filter_by(id=id).first()
        if log_event:
            ret['data'] = log_event.log_info
        else:
            ret['msg'] = '事件不存在'
        return ret


auth_resources = [
    {
        'resource': UserListAPI,
        'urls': '/v1/users'
    },
    {
        'resource': UserAPI,
        'urls': '/v1/users/<int:id>'
    },
    {
        'resource': RoleListAPI,
        'urls': '/v1/roles'
    },
    {
        'resource': RoleAPI,
        'urls': '/v1/roles/<int:id>'
    },
    {
        'resource': MenuListAPI,
        'urls': '/v1/menus'
    },
    {
        'resource': MenuAPI,
        'urls': '/v1/menus/<int:id>'
    },
    {
        'resource': UserLogEventListAPI,
        'urls': '/v1/events'
    },
    {
        'resource': UserLogEventAPI,
        'urls': '/v1/events/<int:id>'
    }
]
