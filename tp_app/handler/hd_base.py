# coding:utf-8
from flask import request, jsonify, make_response, abort
from tp_app import app
import functools


def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                if arg not in request.json:
                    return abort(400)
            return func(*args, **kw)
        return wrapper
    return decorator


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': '参数不正确'}), 400)




