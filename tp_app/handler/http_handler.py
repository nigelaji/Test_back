import json
from flask.app import Response
from werkzeug.exceptions import abort


def self_abort(code: int, msg: str, **kwargs) -> abort:
    ret = {
        "code": code,
        "msg": msg
    }
    return abort(Response(json.dumps(ret), status=200, mimetype='application/json', **kwargs))
