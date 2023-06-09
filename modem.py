import requests
from utils import base64_encode, modem_headers, debug, generateRequestURL, fromHex

ip = "192.168.0.1"
password = "admin"
stok_cookie = None
store_messages = False

def getCookie(cookie = None):
    if not cookie:
        global stok_cookie
        if stok_cookie:
            return stok_cookie
        raise Exception("Cookie not found!")
    return cookie

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
    cookie = getCookie(cookie)
    params = {
        "isTest": 'false',
        'cmd': '%2C'.join(data),
        'multi_data': 1
    }
    url = generateRequestURL("http://%s/goform/goform_get_cmd_process" % ip, params)
    answer = requests.get(url,
        headers = modem_headers | {
            "Referer": "http://%s/index.html" % ip
        },
        cookies=cookie
    )
    debug(f"Get data: {answer}")
    return answer.json()

def getSMSList(cookie = None):
    cookie = getCookie(cookie)
    params = {
        "isTest": 'false',
        'cmd': 'sms_data_total',
        'page': '0',
        'data_per_page': '500',
        'mem_store': '1',
        'tags': '10'
    }
    url = generateRequestURL("http://%s/goform/goform_get_cmd_process" % ip, params)
    url += '&order_by=order+by+id+desc'
    print(url)
    answer = requests.get(url,
        headers = modem_headers | {
            "Referer": "http://%s/index.html" % ip
        },
        cookies=cookie
    )
    debug(f"Get data: {answer}")
    messages = answer.json()['messages']
    toReturn = []
    for i in range(0, len(messages)):
        msg = messages[i]
        msg['content'] = fromHex(msg['content'])
        toReturn.append(msg)
    return toReturn

def getInfo(cookie = None):
    return {
        "main": getSomething(['SSID1', 'AuthMode', 'lan_ipaddr', 'lan_ipaddr', 'wan_ipaddr', 'router_mode_gateway', 'dhcpStart', 'dhcpEnd', 'LocalDomain'], cookie),
        "network": getSomething(['network_type', 'network_provider', 'network_provider_fullname', 'net_select', 'wan_active_band', 'm_profile_name'], cookie),
        "versions": getSomething(['hardware_version', 'web_version', 'wa_inner_version'], cookie),
        "important": getSomething(['imei', 'modem_msn', 'BSSID', 'sim_iccid', 'cell_id', 'sim_imsi', 'rplmn_num', 'enodeb_id'], cookie)
    }