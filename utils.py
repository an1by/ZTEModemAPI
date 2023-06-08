import base64

modem_headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.84 "
                  "Safari/537.36 "
                  "OPR/85.0.4341.60 (Edition Yx 05)",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "dnt": "1",
    "sec-gpc": "1"
}
"""
Headers for every request
"""

def base64_encode(string: str) -> str:
    """
    Base64 encoding function to UTF-8 string
    """
    return str(base64.b64encode(bytes(string, 'utf-8')), encoding='utf-8')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def debug(message: str, type: str = "info", force: bool = False) -> None:
    """
    Logs info to console if variable "debug_feature" if True.
    """
    if ((not debug_feature) and (not force)):
        return
    color = None
    match (type):
        case "success":
            color = bcolors.OKGREEN
        case "warning":
            color = bcolors.WARNING
        case "error" | "fail":
            color = bcolors.FAIL
        case "info" | _:
            color = bcolors.OKCYAN
    print(f"{color}MODEM: {str(message)}{bcolors.ENDC}")

debug_feature = False
"""
Debug logging switcher
"""

from requests.models import PreparedRequest

def generateRequestURL(url: str, params: dict[str, str]) -> str:
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url

def fromHex(text: str):
    res=''
    for i in range(4,len(text),4):
        res += chr(int(text[i-4:i],16))
    return res;