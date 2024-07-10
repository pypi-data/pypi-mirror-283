import json
import base64

from .creator import CDict
from .cookies import Cookies


class Response:
    def __init__(self, r: json):
        self.r = r

    def __build__(self) -> CDict:
        try:
            cookies = Cookies().extract_and_parse_cookies(base64.b64decode(self.r['headers']).decode('utf-8'))
        except:
            cookies = None
        d = {
            "version":  self.r['version'].__str__(),
            "code":     int(self.r['code']),
            "headers":  base64.b64decode(self.r['headers']).decode('utf-8'),
            "body":     base64.b64decode(self.r['body']).decode('utf-8'),
            "cookies":  cookies
        }

        return CDict(d)