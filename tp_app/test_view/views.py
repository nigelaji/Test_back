# coding:utf-8
from flask import jsonify, request, session, Response
from . import test_blue
from tp_app.user_view.auth import require_token


@test_blue.route('/faker', methods=['POST'])
@require_token
def g_faker_data():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    return jsonify(ret)

