import utils

class FakeResponse:

    def __init__(self, status=200, body=""):
        self.status = status
        self.body = body


def test_build_message_success(monkeypatch):
    def fake_request():
        return FakeResponse()
    monkeypatch.setattr('utils.make_request', fake_request)
    result = utils.build_message()
    assert result["success"] is True

#def test_build_message_failure(response):
#    result = build_message(response(400, "not allowed here!"))
#    assert result["success"] is False
#    assert result["error"] == "not allowed here!"
