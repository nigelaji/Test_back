# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_restful import Api
from tp_app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL

app = Flask(__name__)
# 数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 如果没有这行会有警告
app.config["SECRET_KEY"] = "12345678"  # 如果没有，在生成表单的时候，会出现 CRSF 相关错误
app.config['EMAIL_HOST'] = EMAIL_HOST
app.config['EMAIL_PORT'] = EMAIL_PORT
app.config['EMAIL_USE_SSL'] = EMAIL_USE_SSL
app.config['MAIL_USERNAME'] = EMAIL_HOST_USER
app.config['MAIL_PASSWORD'] = EMAIL_HOST_PASSWORD

db = SQLAlchemy()
lm = LoginManager()
db.init_app(app)
lm.init_app(app)
mail = Mail(app)
api = Api(app)

# 创建所有表
with app.app_context():
    from tp_app.models.authModels import User, Role, Menu, user_role, role_menu, UserLogEvent, init_user_role_menu
    from tp_app.models.articleModels import Article, Comment, article_comment, init_article_data

    db.create_all()  # 创建所有表
    init_user_role_menu()
    init_article_data()
# from . import views  # 这里面可以放公共视图

# 注册蓝图
from tp_app.views import user_blue
from tp_app.views import article_blue

# 这个困扰我一天，套他猴子的我，不能写在创建db对象的上边，要不然蓝图中的db就会导入不了
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(article_blue, url_prefix='/article')

from tp_app import views  # 先有app才能导入views
from tp_app.register_api import register_api
register_api(api)