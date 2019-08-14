from page.pingxx import PingxxApi


class ChargeApi(PingxxApi):

    def create(self, data_dict: dict):
        """
        真实的调用 POST /v1/charges 接口
        :param data_dict:  dict
            需要的key
                order_no
                amount,
                channel,
                currency,
                subject,
                body,
                description,
                extra: 需要是个字典，根据 channel
                app: 需要是个字典，{"id": your_app_id}
        :return:
        """
        # 格式化处理请求的数据
        # URI
        req_uri = "/v1/charges"
        # 方法
        req_method = "post"
        # 参数
        req_data = {
            "order_no": data_dict["order_no"]
        }
        # 认证
        req_auth = self.auth
        # cookies
        req_cookies = {}
        # headers
        req_headers = self._get_headers(uri=req_uri, body=req_data)
        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   body=req_data,
                   auth=req_auth,
                   cookies=req_cookies,
                   headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = ["id", "object", "created", "livemode"]
        return self._parse(body_key_list=resp_body_key_list)

    def view(self, id: str):
        # 格式化处理请求的数据
        # URI
        req_uri = ""
        # 方法
        req_method = ""
        # 认证
        req_auth = ""
        # cookies
        req_cookies = {}
        # headers
        req_headers = {}
        # 真正的发请求
        self._send(uri=req_uri, method=req_method, auth=req_auth, cookies=req_cookies, headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = []
        return self._parse(body_key_list=resp_body_key_list)

    def query(self):
        # 格式化处理请求的数据
        # URI
        req_uri = ""
        # 方法
        req_method = ""
        # 认证
        req_auth = ""
        # cookies
        req_cookies = {}
        # headers
        req_headers = {}
        # 真正的发请求
        self._send(uri=req_uri, method=req_method, auth=req_auth, cookies=req_cookies, headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = []
        return self._parse(body_key_list=resp_body_key_list)

    def reverse(self):
        # 格式化处理请求的数据
        # URI
        req_uri = ""
        # 方法
        req_method = ""
        # 认证
        req_auth = ""
        # cookies
        req_cookies = {}
        # headers
        req_headers = {}
        # 真正的发请求
        self._send(uri=req_uri, method=req_method, auth=req_auth, cookies=req_cookies, headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = []
        return self._parse(body_key_list=resp_body_key_list)
