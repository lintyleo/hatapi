# 以下为 业务类使用的 Ping++ 业务基类
from base import read_yaml, parse_dict
from page import BaseApi


class VvtechApi(BaseApi):
    __token = None
    __config = read_yaml(current=__file__, file_path="api.yml", key="VvtechApi")

    def login(self, data_dict: dict):
        """
        登录
        :param data_dict:
        :return:
        """
        req_uri = self._get_config(self.__config, "LOGIN.URI")
        req_method = self._get_config(self.__config, "LOGIN.METHOD")
        req_data = {
            self._get_config(self.__config, "SIGN.BODY_VV_SIGNATURE"): data_dict.get("vv_signature"),
            self._get_config(self.__config, "SIGN.BODY_VV_TIME"): data_dict.get("vv_time"),
            self._get_config(self.__config, "LOGIN.PARAM.PASSWORD"): data_dict.get("password"),
            self._get_config(self.__config, "LOGIN.PARAM.IS_ANDROID"): data_dict.get("is_android"),
            self._get_config(self.__config, "LOGIN.PARAM.CLIENT_ID"): data_dict.get("client_id"),
            self._get_config(self.__config, "LOGIN.PARAM.MOBILE"): data_dict.get("mobile"),
            self._get_config(self.__config, "LOGIN.PARAM.VERSION"): data_dict.get("version")
        }
        req_data = self._remove_none_param(req_data)
        # 认证
        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   data_dict=req_data
                   )
        # 返回响应的结果
        resp_body_key_list = self._get_config(data_dict=self.__config, data_key="LOGIN.RESP.DATA_KEY")
        resp = self._parse(body_key_list=resp_body_key_list)

        data_key_token = self._get_config(self.__config, "LOGIN.RESP.DATA_KEY_TOKEN")
        self.__token = parse_dict(dict_data=resp, data_key=data_key_token)
        return resp

    def _get_body_for_signature(self, token, request_body=None):
        """
        为签名验证构建请求头
        :param uri: URL 去掉 https://{host}，从 / 开始
            注意：GET 请求需要传递全部的 uri，包含请求参数
        :param request_body: 请求的正文，如果没有就不传
        :return: dict
            返回的 字典直接用来做 请求头
            key 列表：
                - PingPlusPlus-Signature
                - PingPlusPlus-Request-Timestamp
        """
        if self.token is None or self.token == "":
            token = self.token
        signature, timestamp = self.request.get_sign_by_md5(
            token=token,
            body_params=request_body
        )
        self.info("[%r] - 获取 VVTECH 验签的请求正文，使用数据 token=%s, params=%r"
                  % (__name__, token, request_body))

        body = {
            self._get_config(data_dict=self.__config, data_key="SIGN.BODY_VV_SIGNATURE"): signature,
            self._get_config(data_dict=self.__config, data_key="SIGN.BODY_VV_TIME"): timestamp
        }

        return body

    @property
    def token(self):
        """
        认证【属性】
        :return:
        """
        return self.__token
