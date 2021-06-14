from flask_restful import Resource


class SelfResource(Resource):
    ret = {
        'code': 200,
        'data': {},
        'msg': 'ok',
    }
