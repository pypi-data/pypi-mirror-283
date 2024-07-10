import re


class Cookies():
    def extract_and_parse_cookies(self, http_header):
        cookies = {}
        cookie_headers = re.findall(r'Set-Cookie:\s*(.*?)(?=\n[A-Z]|\Z)', http_header, re.S)
        for cookie in cookie_headers:
            for item in re.split(r', (?=[^;]+(?:=|$))', cookie.strip()):
                parts = item.split(';')
                name, value = parts[0].split('=', 1)
                attributes = {}
                for attr in parts[1:]:
                    if '=' in attr:
                        key, val = attr.split('=', 1)
                        attributes[key.strip()] = val.strip()
                    else:
                        attributes[attr.strip()] = True
                cookies[name.strip()] = {'value': value.strip(), 'attributes': attributes}
        return cookies

    def cookies_dict_to_header(self, cookies_dict):
        # Join each cookie name and its value (ignoring attributes for the "Cookie" header)
        cookie_header = "; ".join(f"{name}={cookie['value']}" for name, cookie in cookies_dict.items())
        return cookie_header