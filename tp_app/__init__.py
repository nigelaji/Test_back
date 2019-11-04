# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from tp_app.config import ADMIN_MAIL_PASSWORD, ADMIN_MAIL_USERNAME

app = Flask(__name__)
# 数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True         # 如果没有这行会有警告
app.config["SECRET_KEY"] = "12345678"     # 如果没有，在生成表单的时候，会出现 CRSF 相关错误

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ADMIN_MAIL_USERNAME
app.config['MAIL_PASSWORD'] = ADMIN_MAIL_PASSWORD

db = SQLAlchemy()
lm = LoginManager()
db.init_app(app)
lm.init_app(app)
mail = Mail(app)

# 创建所有表
with app.app_context():
    from tp_app.model.userManageModels import User, Role, Menu, user_role, role_menu, UserLogEvent, init_user_role_menu
    db.create_all()     # 创建所有表
    init_user_role_menu()
# from . import views  # 这里面可以放公共视图

# 注册蓝图
from tp_app.user_view import user_blue
# 这个困扰我一天，套他猴子的我，不能写在创建db对象的上边，要不然蓝图中的db就会导入不了
app.register_blueprint(user_blue, url_prefix='/user')

from tp_app import views    # 先有app才能导入views
