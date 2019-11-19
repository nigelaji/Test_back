# coding:utf-8
from flask import Blueprint

test_blue = Blueprint('test', __name__)

from tp_app.test_view import views
