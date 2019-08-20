__version__ = "2.0.2"
__author__ = "ArtLinty"

import json
import time
from enum import Enum

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as SignPKCS115
from requests import Session, Response
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

_CHARACTER_COMMA = ","
_CHARACTER_COLON = ":"
_WAIT_SECONDS = 5
_DEFAULT_ENCODING_UTF8 = "utf-8"
_SUPPORT_METHOD_LIST = ["GET", "POST", "HEAD", "PUT", "DELETE"]


class BoxRequest(object):
    """
    标题： 封装底层 HTTP 库 （request)
    作者： 刘挺立
    时间： 20190815
    邮件： liutingli@ascents.work
    """

    __schema = None
    __host = None
    __port = None
    __headers = None
    __auth = None
    __cookies = None
    __response = None

    class RequestType(Enum):
        """
        请求类型
        """
        HTTP = 1,
        HTTPS = 2

    """
    构造方法
    """

    def __init__(self, schema: RequestType, host: str, port=None):
        """
        构造方法
        :param schema: 请求协议，RequestType 类
        :param host: 主机，支持 主机名称，IP，域名 等
        :param port: 默认为 None，整型
        """
        self.__schema = schema
        self.__host = host
        self.__schema = port
        self.__headers = {}
        self.__cookies = {}

    """
    成员方法
    """

    def send(self, uri: str, method: str,
             data_dict: dict, is_json_content: bool,
             headers=None, cookies=None, auth=None, files=None
             ):
        """
        发送请求
        :param files:
        :param uri:
        :param method:
        :param data_dict:
        :param is_json_content:
        :param headers:
        :param cookies:
        :param auth:
        :return:
        """
        if method is not None and method in _SUPPORT_METHOD_LIST:
            method = method.upper().strip()
        else:
            raise TypeError(
                "请传递一个合法的 HTTP 请求方法, 当前使用的 method = %r"
                % method
            )

        url = self._pre_url(uri=uri, auth=auth)

        if headers is not None and isinstance(headers, dict):
            self.__headers.update(headers)

        if cookies is not None and isinstance(cookies, dict):
            self.__cookies.update(cookies)

        with Session() as s:
            self._request(session=s, method=method, url=url, data_dict=data_dict,
                          is_json_content=is_json_content, files=files)

    def close(self):
        """
        关闭请求，释放请求资源
        :return:
        """
        self.__schema = None
        self.__host = None
        self.__port = None
        self.__auth = None
        self.__cookies = None
        self.__response = None

    @staticmethod
    def get_sign_by_pkcs115(rsa_private_key, uri, body_params):
        """
        根据 私钥，时间戳，uri 和 请求，返回 规定的 headers，使用 pkcs1v15 方法
        :param rsa_private_key: rsa 私钥
        :param uri: URI, api_url 去掉前面的部分
        :param body_params:  api_param
        :return:
        """

        if body_params:
            request_body = json.dumps(body_params).encode(_DEFAULT_ENCODING_UTF8)
            verify_data = [request_body.decode()]
        else:
            verify_data = []
        timestamp = int(time.time())

        verify_data.extend([uri, repr(timestamp)])
        rsa_data = "".join(verify_data)
        rsa_key = RSA.importKey(rsa_private_key)

        signer = SignPKCS115.new(rsa_key)
        msg_hash = SHA256.new(rsa_data.encode(encoding=_DEFAULT_ENCODING_UTF8))
        sign = signer.sign(msg_hash)

        signature = b64encode(sign)
        return signature, str(timestamp)

    """
    属性
    """

    @property
    def json_dict(self):
        """
        数据字典
        :return:
        """

        return self._load_json()

    @property
    def json_format_string(self):
        """
        数据字典
        :return:
        """

        return self._dump_json()

    @property
    def status_code(self):
        """
        状态码
        :return:
        """
        if self.__response is not None and isinstance(self.__response, Response):
            return self.__response.status_code

        return None

    @property
    def cookies(self):
        """
        状态码
        :return:
        """
        if self.__response is not None and isinstance(self.__response, Response):
            return dict(self.__response.cookies)

        return None

    @property
    def response_dict(self):
        """
        响应字典
        :return:
        """
        if self.__response is not None and isinstance(self.__response, Response):
            return dict(
                status_code=self.__response.status_code,
                cookies=dict(self.__response.cookies),
                encoding=str(self.__response.encoding),
                elapsed=self.__response.elapsed.microseconds,
                headers=dict(self.__response.headers),
                reason=self.__response.reason,
                request=str(self.__response.request),
                url=self.__response.url,
                text=self.__response.text,
                ok=self.__response.ok,
                json_dict=self._load_json(),
                json_string=self._dump_json()
            )

        return None

    """
    私有方法
    """

    def _pre_url(self, uri, auth=None):
        """
        请求前置操作
        :param uri:
        :param auth:
        :return:
        """
        if auth:
            if isinstance(auth, tuple) and len(auth) == 2:
                # special-case basic HTTP auth
                self.__auth = HTTPBasicAuth(*auth)
            elif isinstance(auth, dict):
                auth_headers = {auth["key"]: auth["value"]}
                self.__headers.update(auth_headers)
            elif isinstance(auth, str):
                auth_headers = dict(Authorization=auth)
                self.__headers.update(auth_headers)

        url = None
        if self.__schema == self.RequestType.HTTP:
            url = "http://"
        if self.RequestType.HTTPS:
            url = "https://"

        if self.__host.endswith("/"):
            self.__host = self.__host[0:len(self.__host) - 1]

        if self.__port:
            url = "%s%s:%d%s" % (url, self.__host, self.__port, uri)
        else:
            url = url + self.__host + uri
        return url

    def _request(self, session: Session,
                 url: str, method: str, data_dict: dict, is_json_content: bool, files=None):
        """
        具体发送请求
        :param session:
        :return:
        """
        params = jsons = data = None
        if method.lower() in ("get", "delete", "head"):
            params = data_dict
        elif method.lower() in ("post", "put"):
            if is_json_content:
                jsons = data_dict
            else:
                data = data_dict

        if session is not None:
            self.__response = session.request(
                method=method.upper(),
                url=url,
                headers=self.__headers,
                cookies=self.__cookies,
                auth=self.__auth,
                data=data,
                params=params,
                json=jsons,
                files=files,
                verify=False
            )

    def _dump_json(self):
        """
        字典 dict 转为 json
        :return:
        """
        json_string = json.dumps(self._load_json(),
                                 indent=4,
                                 separators=(_CHARACTER_COMMA, _CHARACTER_COLON))
        if json_string is not None and isinstance(json_string, str):
            return json_string.encode('utf-8').decode('unicode_escape')

        return json_string

    def _load_json(self):
        """

        :return:
        """
        r = self.__response
        res_json = None
        if r is not None and isinstance(r, Response):
            try:
                res_json = r.json()

            except Exception as e:
                if r.text and r.text.startswith("{"):
                    res_json = json.loads(r.text)
                print("Response 对象调用 json() 发生异常，请抓包 HTTP 来查看原因: %r" % e)

        return res_json
