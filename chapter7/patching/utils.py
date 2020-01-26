from urllib import request

def make_request():
    response = request.urlopen('http://api.example.com/')
    response.body = response.read()
    return response

def build_message():
    response = make_request()
    message = {
        "success": True,
        "error": "",
    }
    if response.status >= 400:
        message["success"] = False
        message["error"] = response.body
    return message
