# coding:utf-8
from flask import Blueprint

user_blue = Blueprint('user', __name__)

from tp_app.user_view import auth, views
