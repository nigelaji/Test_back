# coding:utf-8
from tp_app import db, lm
from flask_login import UserMixin
from datetime import datetime
from tp_app.common.security import encrypt_with_salt


class User(UserMixin, db.Model):
    """用户表"""
    __tablename__ = 'tp_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, comment='昵称')
    user_code = db.Column(db.String(64), unique=True, comment='用户账号，可用于登录')
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True, comment='一般登录用')
    phone = db.Column(db.String(64), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True)		# index=True，查询用户列表时，加快速度
    status = db.Column(db.CHAR(1), default=1, comment='软删除,0已删除，1正常状态，默认值1')
    locked = db.Column(db.CHAR(1), default=1, comment='锁定用户，0被锁定，1解锁状态，默认值1')
    locked_time = db.Column(db.DateTime)
    unlocked_time = db.Column(db.DateTime)
    login_fail = db.Column(db.Integer, default=0, comment='记录登录失败次数，进行锁定账户')
    remark = db.Column(db.String(500))
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    @staticmethod
    def init_admin():		# 初始化管理员用户
        user = User.query.filter_by(emai='838863149@qq.com').first()
        if not user:
            user = User(username='大佬', user_code='admin', password='123456', emai='838863149@qq.com')		# 为啥是警告？
            db.session.add(user)
            db.session.commit()
            print("初始化管理员账号！")
    
    @property
    def password_hashlib(self):
        raise AttributeError("密码是不可读的属性")
    
    @password_hashlib.setter
    def password_hashlib(self, password):		# 插入密码时，自动加密
        self.password = encrypt_with_salt(password)
    
    def __repr__(self):
        return "<User (username='%r', status='%r')>" % (self.username, self.status)


@lm.user_loader
def load_user(user_id): 		# 必须提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象
    return User.query.get(int(user_id)) 		# id默认传入的是字符串所以要int下


user_role = db.Table('tp_user_role',		# 用户角色关联表
                     db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
                     )


class Role(db.Model):
    """角色表"""
    __tablename__ = 'tp_role'
    id = db.Column(db.Integer, primary_key=True, comment='角色id，主键，自增')
    role_name = db.Column(db.String(20), unique=True, comment='角色名称')
    introduction = db.Column(db.String(200), comment='角色介绍')
    users = db.relationship('User', secondary=user_role, backref=db.backref('role', lazy='dynamic'))
    # Role.users	User.role
    
    def __init__(self, role_name):
        self.role_name = role_name
        
    @staticmethod
    def init_role():
        print('初始化角色表数据')
        role = Role.query.filter_by(role_name='超级管理员').first()
        if not role:
            role = Role(role_name='超级管理员', introduction='最高权限角色')
            db.session.add(role)
            db.session.commit()
    
    def __repr__(self):
        return "<Role (role_name='%r')> " % self.role_name


role_menu = db.Table('tp_role_menu',		# 角色菜单关联表
                     db.Column('role_id', db.Integer, db.ForeignKey('Role.id')),
                     db.Column('menu_id', db.Integer, db.ForeignKey('Menu.id')),
                     )


class Menu(db.Model):
    """菜单表"""
    __tablename__ = 'tp_menu'
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(20))
    menu_url = db.Column(db.String(100), comment='菜单路由')
    icon_class = db.Column(db.String(50), comment='菜单图标')
    status = db.Column(db.CHAR(1),default=1, comment='软删除,0已删除，1正常状态，默认1')
    parent_id = db.Column(db.Integer, default=None, comment='父级菜单id')
    roles = db.relationship('Role', secondary=role_menu, backref=db.backref('menus', lazy='dynamic'))
    # Menu.roles    Role.menus
    
    def __init__(self, menu_name, menu_url):
        self.menu_name = menu_name
        self.menu_url = menu_url
        
    def __repr__(self):
        return "<Menu (menu_name='%r')>" % self.menu_name


class UserLogEvent(db.Model):
    """用户登录事件记录"""
    __tablename__ = 'tp_user_log_event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    client_ip = db.Column(db.String(30), comment='客户端IP')
    log_event = db.Column(db.String(30), comment='事件代码，例：login、logout、login_fail等')
    log_time = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return "<UserLogInOut (user_id='%r', log_event='%r', log_time='%r')> " % (self.user_id, self.log_event, self.log_time)


def init_user_role_menu():		# 对关联表进行数据初始化
    User.init_admin()
    Role.init_role()



