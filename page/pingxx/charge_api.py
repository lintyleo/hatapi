from base import read_yaml, encode_url
from page.pingxx.api import PingxxApi


class ChargeApi(PingxxApi):
    """
    标题： 业务类，普通支付模块的所有接口
    作者： 刘挺立
    日期： 20190819
    邮件： liutingli@ascents.work
    """
    __config = read_yaml(current=__file__, file_path="api.yml", key="ChargeApi")

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
        req_uri = self._get_config(self.__config, "CREATE.URI")
        req_method = self._get_config(self.__config, "CREATE.METHOD")
        req_data = {
            self._get_config(self.__config, "CREATE.PARAM.APP"): data_dict.get("app"),
            self._get_config(self.__config, "CREATE.PARAM.ORDER_NO"): data_dict.get("order_no"),
            self._get_config(self.__config, "CREATE.PARAM.CHANNEL"): data_dict.get("channel"),
            self._get_config(self.__config, "CREATE.PARAM.AMOUNT"): data_dict.get("amount"),
            self._get_config(self.__config, "CREATE.PARAM.CLIENT_IP"): data_dict.get("client_ip"),
            self._get_config(self.__config, "CREATE.PARAM.CURRENCY"): data_dict.get("currency"),
            self._get_config(self.__config, "CREATE.PARAM.SUBJECT"): data_dict.get("subject"),
            self._get_config(self.__config, "CREATE.PARAM.BODY"): data_dict.get("body"),
            self._get_config(self.__config, "CREATE.PARAM.DESCRIPTION"): data_dict.get("description"),
            self._get_config(self.__config, "CREATE.PARAM.EXTRA"): data_dict.get("extra")
        }
        req_data = self._remove_none_param(req_data)
        # 认证
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri, request_body=req_data)
        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   data_dict=req_data,
                   auth=req_auth,
                   cookies=req_cookies,
                   headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = self._get_config(self.__config, "CREATE.RESP.DATA_KEY")
        return self._parse(body_key_list=resp_body_key_list)

    def view(self, charge_id: str):
        """
        真实的调用 GET /v1/charges/{charge_id} 接口
        :param charge_id:
        :return:
        """
        # 格式化处理请求的数据
        req_uri = self._get_config(self.__config, "VIEW.URI") % charge_id
        req_method = self._get_config(self.__config, "VIEW.METHOD")
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   auth=req_auth,
                   cookies=req_cookies,
                   headers=req_headers)
        resp_body_key_list = self._get_config(self.__config, "VIEW.RESP.DATA_KEY")
        return self._parse(body_key_list=resp_body_key_list)

    def query(self, data_dict: dict):
        """
        真实的调用 GET /v1/charges/xxxx=xxxx 接口
        :param data_dict:
        :return:
        """
        # 格式化处理请求的数据
        req_uri = self._get_config(self.__config, "VIEW.URI")
        req_method = self._get_config(self.__config, "VIEW.METHOD")
        req_data = {
            self._get_config(self.__config, "CREATE.PARAM.APP.get(id)"): data_dict.get("app"),
            self._get_config(self.__config, "CREATE.PARAM.LIMIT"): data_dict.get("limit"),
            self._get_config(self.__config, "CREATE.PARAM.CHANNEL"): data_dict.get("channel"),
            self._get_config(self.__config, "CREATE.PARAM.REFUNDED"): data_dict.get("refunded"),
            self._get_config(self.__config, "CREATE.PARAM.REVERSED"): data_dict.get("reversed"),
            self._get_config(self.__config, "CREATE.PARAM.PAID"): data_dict.get("paid"),
            self._get_config(self.__config, "CREATE.PARAM.CREATED_GT"): data_dict.get("created_gt"),
            self._get_config(self.__config, "CREATE.PARAM.CREATED_LT"): data_dict.get("created_lt"),
            self._get_config(self.__config, "CREATE.PARAM.CREATED_GTE"): data_dict.get("created_gte"),
            self._get_config(self.__config, "CREATE.PARAM.CREATED_LTE"): data_dict.get("created_lte")
        }
        req_data = self._remove_none_param(req_data)
        req_uri = encode_url(url=req_uri, params=req_data)
        req_auth = self.auth

        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   auth=req_auth,
                   cookies=req_cookies,
                   headers=req_headers)
        resp_body_key_list = self._get_config(self.__config, "VIEW.RESP.DATA_KEY")
        return self._parse(body_key_list=resp_body_key_list)

    def reverse(self, charge_id):
        """
        真实的调用 POST .v1.charges.{charge_id}.reverse 接口
        :param charge_id:
        :return:
        """
        # 格式化处理请求的数据
        # URI
        # 格式化处理请求的数据
        req_uri = self._get_config(self.__config, "REVERSE.URI") % charge_id
        req_method = self._get_config(self.__config, "REVERSE.METHOD")
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   auth=req_auth,
                   cookies=req_cookies,
                   headers=req_headers)
        resp_body_key_list = self._get_config(self.__config, "REVERSE.RESP.DATA_KEY")
        return self._parse(body_key_list=resp_body_key_list)
