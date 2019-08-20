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
        req_uri = self.get_config(self.__config, "CREATE/URI")
        req_method = self.get_config(self.__config, "CREATE/METHOD")
        req_data = {
            self.get_config(self.__config, "CREATE/PARAM/APP"): data_dict["app"],
            self.get_config(self.__config, "CREATE/PARAM/ORDER_NO"): data_dict["order_no"],
            self.get_config(self.__config, "CREATE/PARAM/CHANNEL"): data_dict["channel"],
            self.get_config(self.__config, "CREATE/PARAM/AMOUNT"): data_dict["amount"],
            self.get_config(self.__config, "CREATE/PARAM/CLIENT_IP"): data_dict["client_ip"],
            self.get_config(self.__config, "CREATE/PARAM/CURRENCY"): data_dict["currency"],
            self.get_config(self.__config, "CREATE/PARAM/SUBJECT"): data_dict["subject"],
            self.get_config(self.__config, "CREATE/PARAM/BODY"): data_dict["body"],
            self.get_config(self.__config, "CREATE/PARAM/DESCRIPTION"): data_dict["description"],
            self.get_config(self.__config, "CREATE/PARAM/EXTRA"): data_dict["extra"]}
        # 认证
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri, request_body=req_data)
        # 真正的发请求
        self.send(uri=req_uri,
                  method=req_method,
                  data_dict=req_data,
                  auth=req_auth,
                  cookies=req_cookies,
                  headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = self.get_config(self.__config, "CREATE/RESP/DATA_KEY")
        return self.parse(body_key_list=resp_body_key_list)

    def view(self, charge_id: str):
        # 格式化处理请求的数据
        req_uri = self.get_config(self.__config, "VIEW/URI") % charge_id
        req_method = self.get_config(self.__config, "VIEW/METHOD")
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self.send(uri=req_uri,
                  method=req_method,
                  auth=req_auth,
                  cookies=req_cookies,
                  headers=req_headers)
        resp_body_key_list = self.get_config(self.__config, "VIEW/RESP/DATA_KEY")
        return self.parse(body_key_list=resp_body_key_list)

    def query(self, data_dict: dict):
        # 格式化处理请求的数据
        req_uri = self.get_config(self.__config, "VIEW/URI")
        req_method = self.get_config(self.__config, "VIEW/METHOD")
        req_data = {
            self.get_config(self.__config, "CREATE/PARAM/APP[id]"): data_dict["app"],
            self.get_config(self.__config, "CREATE/PARAM/LIMIT"): data_dict["limit"],
            self.get_config(self.__config, "CREATE/PARAM/CHANNEL"): data_dict["channel"],
            self.get_config(self.__config, "CREATE/PARAM/REFUNDED"): data_dict["refunded"],
            self.get_config(self.__config, "CREATE/PARAM/REVERSED"): data_dict["reversed"],
            self.get_config(self.__config, "CREATE/PARAM/PAID"): data_dict["paid"],
            self.get_config(self.__config, "CREATE/PARAM/CREATED_GT"): data_dict["created_gt"],
            self.get_config(self.__config, "CREATE/PARAM/CREATED_LT"): data_dict["created_lt"],
            self.get_config(self.__config, "CREATE/PARAM/CREATED_GTE"): data_dict["created_gte"],
            self.get_config(self.__config, "CREATE/PARAM/CREATED_LTE"): data_dict["created_lte"]
        }
        req_uri = encode_url(url=req_uri, params=req_data)
        req_auth = self.auth

        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self.send(uri=req_uri,
                  method=req_method,
                  auth=req_auth,
                  cookies=req_cookies,
                  headers=req_headers)
        resp_body_key_list = self.get_config(self.__config, "VIEW/RESP/DATA_KEY")
        return self.parse(body_key_list=resp_body_key_list)

    def reverse(self, charge_id):
        # 格式化处理请求的数据
        # URI
        # 格式化处理请求的数据
        req_uri = self.get_config(self.__config, "REVERSE/URI") % charge_id
        req_method = self.get_config(self.__config, "REVERSE/METHOD")
        req_auth = self.auth
        req_cookies = {}
        req_headers = self._get_headers_for_signature(uri=req_uri)

        # 真正的发请求
        self.send(uri=req_uri,
                  method=req_method,
                  auth=req_auth,
                  cookies=req_cookies,
                  headers=req_headers)
        resp_body_key_list = self.get_config(self.__config, "REVERSE/RESP/DATA_KEY")
        return self.parse(body_key_list=resp_body_key_list)
