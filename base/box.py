from enum import Enum

from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


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

    def send(self, url: str, method: str,
             data_dict: dict, is_json_content: bool,
             headers=None, cookies=None, auth=None, files=None
             ):
        """
        发送请求
        :param url:
        :param method:
        :param data_dict:
        :param is_json_content:
        :param headers:
        :param cookies:
        :param auth:
        :return:
        """

    def _pre_send(self, uri, auth=None):
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
                auth_headers = {auth["key"]:auth["value"]}
                self.__headers.update(auth_headers)
            elif isinstance(auth, str):
                auth_headers = dict(Authorization=auth)
                self.__headers.update(auth_headers)

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

    def _request(self, session: Session,
                 url: str, method: str, data_dict: dict, is_json_content: bool, headers=None):
        """
        具体发送请求
        :param session:
        :return:
        """
        params = json = data = None
        if method.lower() in ("get", "delete", "head"):
            params = data_dict
        elif method.lower() in ("post", "put"):
            if is_json_content:
                json = data_dict
            else:
                data = data_dict

        if session is not None:
            self.__response = session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                cookies=self.__cookies,
                auth=self.__auth,
                data=data,
                params=params,
                json=json,
                verify=False
            )
