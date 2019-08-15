import json
from enum import Enum

from requests import Session, Response
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

_CHARACTER_COMMA = ","
_CHARACTER_COLON = ":"
_WAIT_SECONDS = 3
_DEFAULT_ENCODING_UTF8 = "utf-8"


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

    class RequestSchema(Enum):
        """
        请求类型
        """
        HTTP = 1,
        HTTPS = 2

    class RequestMethod(Enum):
        """
        请求类型
        """
        GET = 1,
        POST = 2,
        PUT = 3,
        DELETE = 4,
        HEAD = 2

    def __init__(self, schema: RequestSchema, host: str, port=None):
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

    def send(self, uri: str, method: RequestMethod,
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

        url = self._pre_url(uri=uri, auth=auth)
        request_method = self._pre_method(method=method)

        if headers is not None and isinstance(headers, dict):
            self.__headers.update(headers)

        if cookies is not None and isinstance(cookies, dict):
            self.__cookies.update(cookies)

        with Session() as s:
            self._request(session=s, method=request_method, url=url, data_dict=data_dict,
                          is_json_content=is_json_content, files=files)

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
        if self.__schema == self.RequestSchema.HTTP:
            url = "http://"
        if self.RequestSchema.HTTPS:
            url = "https://"

        if self.__host.endswith("/"):
            self.__host = self.__host[0:len(self.__host) - 1]

        if self.__port:
            url = "%s%s:%d%s" % (url, self.__host, self.__port, uri)
        else:
            url = url, self.__host, uri
        return url

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

    def _pre_method(self, method: RequestMethod):
        """
        处理请求方法
        :param method:
        :return:
        """
        m = "POST"
        if method == self.RequestMethod.GET:
            m = "GET"
        elif method == self.RequestMethod.POST:
            m = "POST"
        elif method == self.RequestMethod.HEAD:
            m = "HEAD"
        elif method == self.RequestMethod.PUT:
            m = "PUT"
        elif method == self.RequestMethod.DELETE:
            m = "DELETE"

        return m

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
