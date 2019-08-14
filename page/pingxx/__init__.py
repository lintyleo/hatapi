from page import BaseApi
from page.pingxx.charge_api import ChargeApi


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


class PingxxApi(BaseApi):
    __auth = None
    __rsa_private = None

    def __init__(self, secret_key, rsa_private=None):
        """
        构造 PingxxApi 的方法
        :param secret_key: 开发密钥
        :param rsa_private:  RSA商户私钥（需要整个字符串文本）
        """
        self.__auth = (secret_key, "")
        self.__rsa_private = rsa_private

    def _get_headers(self, uri, body=None):
        return {}

    @property
    def auth(self):
        return self.__auth
