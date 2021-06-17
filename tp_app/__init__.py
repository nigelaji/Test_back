# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # https://docs.sqlalchemy.org/en/14/core/expression_api.html
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
app.config['SQLALCHEMY_ECHO']=True  # 查看执行的sql语句输出
# app.config['FLASKY_DB_QUERY_TIMEOUT'] = 0.0001  # 设置sql执行超时时间，#记录执行时间超过 0.0001秒的
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 断开设置
# app.config['SQLALCHEMY_RECORD_QUERIES'] = True  # 启用慢查询记录功能

login = LoginManager()
db.init_app(app)
login.init_app(app) # 默认情况下，Flask-Login 使用 session 进行身份验证。
mail = Mail(app)
api = Api(app)

# 创建所有表
with app.app_context():
    from tp_app.models.authModels import User, Role, Menu, user_role, role_menu, UserLogEvent, init_user_role_menu
    from tp_app.models.articleModels import Article, Comment, article_comment, init_article_data
    from tp_app.models.hostModels import Host, init_host_data

    db.create_all()  # 创建所有表
    init_user_role_menu()
    init_article_data()
    init_host_data()
# from . import views  # 这里面可以放公共视图

# 注册蓝图
from tp_app.views import user_blue
from tp_app.views import article_blue
from tp_app.restapis import restful_blue

# 这个困扰我一天，套他猴子的我，不能写在创建db对象的上边，要不然蓝图中的db就会导入不了
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(article_blue, url_prefix='/article')

from tp_app import views  # 先有app才能导入views
from tp_app.register_api import register_api
register_api(api)
app.register_blueprint(restful_blue, url_prefix='/rest')    # url_prefix 目前这个没生效
