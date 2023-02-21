import app.utils.util as util
from run import app


def test_is_uuid_success():
    result = util.is_uuid("566f2ece-d0b0-4c3b-b5a0-c1ad2fb6d346")
    assert result == True


def test_is_uuid_fail():
    result = util.is_uuid("abcd")
    assert result == False


def test_send_json():
    data = [{"user_id": 1}]
    with app.app_context():
        res = util.send_json(data)
        assert res.status_code == 200


def test_send_json_404():
    data = [{"user_id": 1}]
    status_code = 404
    with app.app_context():
        res = util.send_json(data, status_code)
        assert res.status_code == status_code
        assert res.data == b'[{"user_id": 1}]'


def test_json_error():
    data = {"message": "internal server error"}
    status_code = 500
    with app.app_context():
        res = util.json_error(status_code, data)
        assert res.status_code == status_code
        assert res.data == b'{"message":"internal server error"}\n'
