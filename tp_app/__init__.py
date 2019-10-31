# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# 数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True         # 如果没有这行会有警告
app.config["SECRET_KEY"] = "12345678"     # 如果没有，在生成表单的时候，会出现 CRSF 相关错误
db = SQLAlchemy()
lm = LoginManager()
db.init_app(app)
lm.init_app(app)
# 创建所有表
with app.app_context():
    db.create_all()     # 创建所有表
# init_user_role_menu()
# from . import views  # 这里面可以放公共视图

# 注册蓝图
from tp_app.user_view import user_blue
# 这个困扰我一天，套他猴子的我，不能写在创建db对象的上边，要不然蓝图中的db就会导入不了
app.register_blueprint(user_blue, url_prefix='/user')

from tp_app import views    # 先有app才能导入views
