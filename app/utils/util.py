import json
from uuid import UUID

import flask


def is_uuid(id):
    try:
        UUID(id)
        return True
    except Exception:
        return False


def send_json(data: list, status_code=200):
    data = json.dumps(data)
    return flask.current_app.make_response(
        (data, status_code, {"Content-Type": "application/json"})
    )


def json_error(code, eror_dict):
    response = flask.jsonify(eror_dict)
    response.status_code = code
    return response
