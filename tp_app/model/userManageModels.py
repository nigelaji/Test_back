# coding:utf-8
from tp_app import db, lm
from flask_login import UserMixin
from datetime import datetime
from tp_app.common.security import encrypt_with_salt


def dump_datetime(value):
    """处理DateTime格式的字段，处理成json容易处理的"""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


user_role = db.Table('tp_user_role',		# 用户角色关联表
                     db.Column('user_id', db.Integer, db.ForeignKey('tp_user.id')),     # 必须是真实表名.id，当然也可以是类名前提是__tablename__不写
                     db.Column('role_id', db.Integer, db.ForeignKey('tp_role.id'))
                     )


class User(UserMixin, db.Model):
    """用户表"""
    __tablename__ = 'tp_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, comment='昵称')
    user_code = db.Column(db.String(64), unique=True, comment='用户账号，可用于登录')
    password_hashlib = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True, comment='一般登录用')
    phone = db.Column(db.String(64), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True)		# index=True，查询用户列表时，加快速度
    status = db.Column(db.CHAR(1), default=1, comment='软删除,0已删除，1正常状态，默认值1')
    locked = db.Column(db.CHAR(1), default=1, comment='锁定用户，0被锁定，1解锁状态，默认值1')
    locked_time = db.Column(db.DateTime, default=None)
    unlocked_time = db.Column(db.DateTime, default=None)
    login_fail = db.Column(db.Integer, default=0, comment='记录登录失败次数，进行锁定账户')
    remark = db.Column(db.String(500))
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError("密码是不可读的属性")

    @password.setter
    def password(self, password):  # 插入明文密码时，自动加密
        self.password_hashlib = encrypt_with_salt(password)
    
    def __init__(self, username, password, email, user_code=None, phone=None, remark=None):
        self.username = username
        self.password = password
        self.email = email
        self.user_code = user_code
        self.phone = phone
        self.remark = remark
    
    @staticmethod
    def init_admin():		# 初始化管理员用户
        user = User.query.filter_by(email='838863149@qq.com').first()
        if not user:
            print('初始化用户表')
            user1 = User(username='超级管理员', password='123456', email='838863149@qq.com', user_code='super_admin')  # 有__init__方法才能这样写
            user2 = User(username='管理员', password='123456', email='admin@qq.com', user_code='admin')
            user3 = User(username='普通用户', password='123456', email='guest@qq.com', user_code='guest')
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()
    
    def __repr__(self):
        return "<User (username='%r', status='%r')>" % (self.username, self.status)

    @property
    def person_info(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_code': self.user_code,
            'email': self.email,
            'phone': self.phone,
            'create_time': dump_datetime(self.create_time),
            # 'update_time': dump_datetime(self.update_time),
            'locked': self.locked,
            # 'locked_time': dump_datetime(self.locked_time),
            # 'unlocked_time': dump_datetime(self.unlocked_time),
            'remark': self.remark,
        }
    
    @property
    def serialize(self):
        """直接返回一个简单的序列化json串"""
        if self.status == '0' or self.locked == '0':
            return {'msg': '用户被删除或锁定，联系管理员'}
        return {
            'id': self.id,
            'username': self.username,
            'user_code': self.user_code,
            'email': self.email,
            'phone': self.phone,
            'create_time': dump_datetime(self.create_time),
            'update_time': dump_datetime(self.update_time),
            'locked': self.locked,
            'locked_time': dump_datetime(self.locked_time),
            'unlocked_time': dump_datetime(self.unlocked_time),
            'remark': self.remark,
            'roles': [role.serialize for role in self.roles],
        }


# @lm.user_loader
# def load_user(user_id): 		# 必须提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象
#     return User.query.get(int(user_id)) 		# id默认传入的是字符串所以要int下


role_menu = db.Table('tp_role_menu',		# 角色菜单关联表
                     db.Column('role_id', db.Integer, db.ForeignKey('tp_role.id')),
                     db.Column('menu_id', db.Integer, db.ForeignKey('tp_menu.id')),
                     )


class Role(db.Model):
    """角色表"""
    __tablename__ = 'tp_role'
    id = db.Column(db.Integer, primary_key=True, comment='角色id，主键，自增')
    role_name = db.Column(db.String(20), unique=True, comment='角色名称')
    role_level = db.Column(db.Integer, unique=True, comment='角色等级')     # 1最高，2中等，3低等
    status = db.Column(db.CHAR(1), default=1, comment='软删除,0已删除，1正常状态，默认值1')
    introduction = db.Column(db.String(200), comment='角色介绍')
    # users = db.relationship('User', secondary=user_role, backref=db.backref('roles', lazy='dynamic'))
    # Role.users	User.role
    menus = db.relationship('Menu', secondary=role_menu, backref=db.backref('roles', lazy='dynamic'))
    
    def __init__(self, role_name, role_level, introduction=None):
        self.role_name = role_name
        self.role_level = role_level
        self.introduction = introduction
    
    @property
    def role_info(self):
        if self.status == '0':
            return {'msg': '角色已被删除'}
        return {
            'id': self.id,
            'role_name': self.role_name,
            'role_level': self.role_level,
            'introduction': self.introduction
        }
    
    @property
    def serialize(self):
        if self.status == '0':
            return {'msg': '角色已被删除'}
        return {
            'id': self.id,
            'role_name': self.role_name,
            'role_level': self.role_level,
            'menus': [menu.serialize for menu in self.menus]
        }
    
    @staticmethod
    def init_role():
        role = Role.query.filter_by(role_name='超级管理员').first()
        if not role:
            print('初始化角色表')
            role1 = Role(role_name='超级管理员', role_level=1, introduction='超级管理员，最高角色权限，一般不外传')
            role2 = Role(role_name='管理员', role_level=2, introduction='企业用户管理员角色使用')
            role3 = Role(role_name='普通用户', role_level=3, introduction='企业下普通用户使用')
            user1 = User.query.filter_by(id=1).first()
            user2 = User.query.filter_by(id=2).first()
            user3 = User.query.filter_by(id=3).first()
            role1.users = [user1]
            role2.users = [user1, user2]
            role3.users = [user1, user2, user3]
            db.session.add(role1)
            db.session.add(role2)
            db.session.add(role3)
            db.session.commit()
    
    def __repr__(self):
        return "<Role (role_name='%r')> " % self.role_name


class Menu(db.Model):
    """菜单表"""
    __tablename__ = 'tp_menu'
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(20))
    menu_url = db.Column(db.String(100), comment='菜单路由')
    icon_class = db.Column(db.String(50), comment='菜单图标', default=None)
    status = db.Column(db.CHAR(1), default=1, comment='软删除,0已删除，1正常状态，默认1')
    parent_id = db.Column(db.Integer, db.ForeignKey("tp_menu.id"))  # 父id
    parent = db.relationship('Menu', remote_side=[id])  # 自关联关系
    # roles = db.relationship('Role', secondary=role_menu, backref=db.backref('menus', lazy='dynamic'))
    # Menu.roles    Role.menus
    
    def __init__(self, menu_name, menu_url, icon_class=None, parent=None):
        self.menu_name = menu_name
        self.menu_url = menu_url
        self.icon_class = icon_class
        self.parent = parent
    
    @property
    def serialize(self):        # 菜单编辑的时候也可以用这个属性
        if self.status == '0':
            return {'msg': '菜单已被删除'}
        return {
            'id': self.id,
            'menu_name': self.menu_name,
            'menu_url': self.menu_url,
            'icon_class': self.icon_class,
            'parent_id': self.parent_id,
        }
    
    def __repr__(self):
        return "<Menu (menu_name='%r')>" % self.menu_name
    
    @staticmethod
    def init_menu():
        menu = Menu.query.filter_by(status='1').all()
        if not menu:
            print("初始化菜单表")
            menu1 = Menu('系统管理', '')
            # db.session.add(menu1)
            # db.session.commit()
            menu2 = Menu(menu_name='用户管理', menu_url='/userManagement', parent=menu1)
            menu3 = Menu(menu_name='角色管理', menu_url='/roleManagement', parent=menu1)
            menu4 = Menu(menu_name='菜单管理', menu_url='/menuManagement', parent=menu1)
            db.session.add(menu1)
            db.session.add(menu2)
            db.session.add(menu3)
            db.session.add(menu4)
            
            menu5 = Menu(menu_name='功能管理', menu_url='')
            menu6 = Menu(menu_name='功能菜单1', menu_url='/funcMenu1', parent=menu5)
            menu7 = Menu(menu_name='功能菜单2', menu_url='/funcMenu2', parent=menu5)
            menu8 = Menu(menu_name='功能菜单3', menu_url='/funcMenu3', parent=menu5)
            db.session.add(menu5)
            db.session.add(menu6)
            db.session.add(menu7)
            db.session.add(menu8)
            
            # 给超级管理员赋权所有菜单
            role1 = Role.query.filter_by(id=1).first()
            role1.menus = [menu1, menu2, menu3, menu4, menu5, menu6, menu7, menu8]
            # 给普通管理员赋权菜单
            role2 = Role.query.filter_by(id=2).first()
            role2.menus = [menu1, menu2, menu5, menu6, menu7, menu8]
            # 给普通用户赋权菜单
            role3 = Role.query.filter_by(id=3).first()
            role3.menus = [menu5, menu6, menu7, menu8]
            db.session.add(role1)
            db.session.add(role2)
            db.session.add(role3)
            db.session.commit()
            


class UserLogEvent(db.Model):
    """用户登录事件记录"""
    __tablename__ = 'tp_user_log_event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    client_ip = db.Column(db.String(30), comment='客户端IP')
    log_event = db.Column(db.String(30), comment='事件代码，例：login、logout、login_fail等')
    log_time = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self, user_id, client_ip, log_event):
        self.user_id = user_id
        self.client_ip = client_ip
        self.log_event = log_event
    
    def __repr__(self):
        return "<UserLogInOut (user_id='%r', log_event='%r', log_time='%r')> " % (self.user_id, self.log_event, self.log_time)


def init_user_role_menu():		# 对关联表进行数据初始化
    User.init_admin()
    Role.init_role()
    Menu.init_menu()
    

