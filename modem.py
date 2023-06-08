import requests
from utils import base64_encode, modem_headers, debug, generateRequestURL

ip = "192.168.0.1"
password = "admin"
stok_cookie = None

def auth(apply = False) -> dict[str, str]:
    """
    Returns cookie (stok) for authentication. While "apply" equals True, stok applies locale.
    """
    global ip, password
    answer = requests.post(
        "http://%s/goform/goform_set_cmd_process" % ip,
        data = {
            'isTest': 'false',
            'goformId': 'LOGIN',
            'password': base64_encode(password)
        },
        headers = modem_headers | {
           "Origin": "http://%s" % ip,
           "Referer": "http://%s/index.html" % ip
        }
    )
    if answer.json()['result'] != "0":
        raise Exception("Auth Error")
    debug(f"Auth: {answer}")
    toReturn = {"stok": answer.cookies.get("stok")}
    if (apply):
        global stok_cookie
        stok_cookie = toReturn
    return toReturn

def getSomething(data: list[str], cookie = None):
    if not cookie:
        global stok_cookie
        if stok_cookie:
            cookie = stok_cookie
        else:
            debug("Cookie not found!", "error", True)
            return
    params = {
        "isTest": 'false',
        'cmd': data,
        'multi_data': 1
    }
    url = generateRequestURL("http://%s/goform/goform_get_cmd_process" % ip, params)
    answer = requests.get(url,
        headers = modem_headers | {
            "Referer": "http://192.168.0.1/index.html"
        },
        cookies=cookie
    )
    debug(f"Get data: {answer}")
    return answer