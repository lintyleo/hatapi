from base import read_yaml
from page import BaseApi
from page.pingxx.charge_api import ChargeApi


# 以下是测试用例使用的场景

def biz_create_charge(data_input_dict: dict):
    """
    场景：创建支付对象的场景，事实上会调用 /v1/charge POST 请求
    :param data_input_dict: dict 必须是字典，至少有以下的 key
        order_no
        amount,
        channel,
        currency,
        subject,
        body,
        description,
        extra,
        app,
        id,
        secret_key,
        request,
        logger
    :return:  字典 dict
        status_code
        接口的默认首层返回值
    """
    # TODO: 场景方法，给测试用例使用，创建支付
    api = ChargeApi(secret_key=data_input_dict["secret_key"])
    data_dict = dict(
        order_no=data_input_dict["order_no"]
    )
    result = api.create(data_dict)

    return result


def biz_view_charge(data_input_dict: dict):
    api = ChargeApi()
    result = api.view()
    return result


def biz_reverse_charge(data_input_dict: dict):
    api = ChargeApi()
    result = api.reverse()
    return result


def biz_query_charge(data_input_dict: dict):
    api = ChargeApi()
    result = api.query()
    return result


def biz_create_and_view_charge(data_input_dict: dict):
    api = ChargeApi()

    result_create = api.create()
    id = result_create["id"]
    result_view = api.view(id)
    return result_create, result_view


# 以下为 业务类使用的 Ping++ 业务基类

class PingxxApi(BaseApi):
    __auth = None
    __rsa_private = None
    __config = read_yaml(current=__file__, file_path="api.yml", key="PingxxApi")

    def __init__(self, request, logger, secret_key: str, rsa_private: str):
        """
        构造 PingxxApi 的方法
        :param secret_key: 开发密钥
        :param rsa_private:  RSA商户私钥（需要整个字符串文本）
        """
        # 调用父类，完成父类的构造方法
        super().__init__(request=request, logger=logger)

        self.__auth = (secret_key, "")
        self.__rsa_private = rsa_private

    def _get_headers_for_signature(self, uri, request_body=None):
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
        signature, timestamp = self.request.get_sign_by_pkcs115(
            rsa_private_key=self.__rsa_private,
            uri=uri,
            body_params=request_body
        )
        self.info("[%r] - 获取 Ping++ 验签的请求头，使用数据 uri=%s, params=%r"
                  % (__name__, uri, request_body))

        headers = {
            self.get_config(config_dict=self.__config, path="SIGN/HEADER_SIGNATURE"): signature,
            self.get_config(config_dict=self.__config, path="SIGN/HEADER_TIMESTAMP"): timestamp
        }

        return headers

    @property
    def auth(self):
        """
        认证【属性】
        :return:
        """
        return self.__auth
