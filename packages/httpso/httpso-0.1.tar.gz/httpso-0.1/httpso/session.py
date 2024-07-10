import base64
import json

import httpso.util    as util

from .cookies       import Cookies
from .creator       import CDict
from .executor      import Executor
from .response      import Response
from urllib.parse   import urlencode

class Session():
    def __init__(self,
                 http_version: int,
                 proxy_host: str = None,
                 proxy_port: int = None,
                 proxy_username: str = None,
                 proxy_password: str = None,
                 ja3_fingerprint: str = None):
        self.http_version       = http_version
        self.proxy_host         = proxy_host
        self.proxy_port         = proxy_port
        self.proxy_username     = proxy_username
        self.proxy_password     = proxy_password
        self.ja3_fingerprint    = ja3_fingerprint

    def __build__(self) -> dict:
        if self.proxy_host is not None:
            self.proxy_host = util.__refactor_proxy_host__(self.proxy_host)
        return {
            "http":             self.http_version,
            "proxy_host":       self.proxy_host if self.proxy_host else "",
            "proxy_port":       self.proxy_port if self.proxy_host else 0,
            "proxy_username":   self.proxy_username if self.proxy_username else "",
            "proxy_password":   self.proxy_password if self.proxy_password else "",
            "ja3":              self.ja3_fingerprint if self.ja3_fingerprint else "",
        }

    def get(self, url: str, headers: dict = None, cookies: dict = None,  timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "GET"
        params['url'] = url
        if headers:
            if cookies:
                headers['cookies'] = Cookies().cookies_dict_to_header(cookies)
            if self.http_version == 2:  # HTTP 2 needs lower case keys
                params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
            else:
                params['headers'] = urlencode(headers)
        else:
            if cookies:
                headers = {'cookies': Cookies().cookies_dict_to_header(cookies)}
                if self.http_version == 2:  # HTTP 2 needs lower case keys
                    params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
                else:
                    params['headers'] = urlencode(headers)
            params['headers'] = ""
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def delete(self, url: str, timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "DELETE"
        params['url'] = url
        params['headers'] = ""
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def head(self, url: str, timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "HEAD"
        params['url'] = url
        params['headers'] = ""
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def trace(self, url: str, timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "TRACE"
        params['url'] = url
        params['headers'] = ""
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def post(self, url: str, headers: dict = None, data = None, json: json = None, cookies: dict = None,  timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "POST"
        params['url'] = url
        if headers:
            if cookies:
                headers['cookies'] = Cookies().cookies_dict_to_header(cookies)
            if self.http_version == 2:  # HTTP 2 needs lower case keys
                params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
            else:
                params['headers'] = urlencode(headers)
        else:
            if cookies:
                headers = {'cookies': Cookies().cookies_dict_to_header(cookies)}
                if self.http_version == 2:  # HTTP 2 needs lower case keys
                    params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
                else:
                    params['headers'] = urlencode(headers)
            params['headers'] = ""
        if not data and not json:
            raise Exception(f"{params['request']} request requires either data or json")
        if data and json:
            raise Exception(f"Please pass either data or json")
        if data:
            if util.__check_is_hex_string__(data): # Hex
                params['payload'] = base64.b64encode(bytes.fromhex(data)).decode("utf-8")
            elif util.__check_is_bytes__(data): # Bytes
                params['payload'] = base64.b64encode(data).decode("utf-8")
            else: # String
                params['payload'] = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        if json:
            params['payload'] = base64.b64encode(json.encode("utf-8")).decode("utf-8")
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def put(self, url: str, headers: dict = None, data: str = None, json: json = None, cookies: dict = None,  timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "PUT"
        params['url'] = url
        if headers:
            if cookies:
                headers['cookies'] = Cookies().cookies_dict_to_header(cookies)
            if self.http_version == 2:  # HTTP 2 needs lower case keys
                params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
            else:
                params['headers'] = urlencode(headers)
        else:
            if cookies:
                headers = {'cookies': Cookies().cookies_dict_to_header(cookies)}
                if self.http_version == 2:  # HTTP 2 needs lower case keys
                    params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
                else:
                    params['headers'] = urlencode(headers)
            params['headers'] = ""
        if not data and not json:
            raise Exception(f"{params['request']} request requires either data or json")
        if data and json:
            raise Exception(f"Please pass either data or json")
        if data:
            if util.__check_is_hex_string__(data):  # Hex
                params['payload'] = base64.b64encode(bytes.fromhex(data)).decode("utf-8")
            elif util.__check_is_bytes__(data):  # Bytes
                params['payload'] = base64.b64encode(data).decode("utf-8")
            else:  # String
                params['payload'] = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        if json:
            params['payload'] = base64.b64encode(json.encode("utf-8")).decode("utf-8")
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()

    def patch(self, url: str, headers: dict = None, data: str = None, json: json = None, cookies: dict = None, timeout: int = 30, tls_server: str = None, tls_port: int = 443) -> CDict:
        params = self.__build__()
        params['request'] = "PATCH"
        params['url'] = url
        if headers:
            if cookies:
                headers['cookies'] = Cookies().cookies_dict_to_header(cookies)
            if self.http_version == 2:  # HTTP 2 needs lower case keys
                params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
            else:
                params['headers'] = urlencode(headers)
        else:
            if cookies:
                headers = {'cookies': Cookies().cookies_dict_to_header(cookies)}
                if self.http_version == 2:  # HTTP 2 needs lower case keys
                    params['headers'] = urlencode(util.__lower_case_dict_values__(headers))
                else:
                    params['headers'] = urlencode(headers)
            params['headers'] = ""
        if not data and not json:
            raise Exception(f"{params['request']} request requires either data or json")
        if data and json:
            raise Exception(f"Please pass either data or json")
        if data:
            if util.__check_is_hex_string__(data):  # Hex
                params['payload'] = base64.b64encode(bytes.fromhex(data)).decode("utf-8")
            elif util.__check_is_bytes__(data):  # Bytes
                params['payload'] = base64.b64encode(data).decode("utf-8")
            else:  # String
                params['payload'] = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        if json:
            params['payload'] = base64.b64encode(json.encode("utf-8")).decode("utf-8")
        params['timeout'] = timeout
        if not tls_server:
            params['server'] = util.__www_subdomain__(url)
        else:
            params['server'] = tls_server
        params['port'] = tls_port

        # Execute request
        r = Executor().run(params)

        # Return parsed response
        return Response(r).__build__()
