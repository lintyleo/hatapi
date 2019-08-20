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
    api = ChargeApi(secret_key=data_input_dict["secret_key"],
                    rsa_private=data_input_dict["rsa_private"],
                    request=data_input_dict["request"],
                    logger=data_input_dict["logger"]
                    )

    result = api.create(data_input_dict)

    return result


def biz_view_charge(data_input_dict: dict):
    api = ChargeApi(secret_key=data_input_dict["secret_key"],
                    rsa_private=data_input_dict["rsa_private"],
                    request=data_input_dict["request"],
                    logger=data_input_dict["logger"])
    result = api.view(data_input_dict["charge_id"])
    return result


def biz_reverse_charge(data_input_dict: dict):
    api = ChargeApi(secret_key=data_input_dict["secret_key"],
                    rsa_private=data_input_dict["rsa_private"],
                    request=data_input_dict["request"],
                    logger=data_input_dict["logger"])
    result = api.reverse(data_input_dict["charge_id"])
    return result


def biz_query_charge(data_input_dict: dict):
    api = ChargeApi(secret_key=data_input_dict["secret_key"],
                    rsa_private=data_input_dict["rsa_private"],
                    request=data_input_dict["request"],
                    logger=data_input_dict["logger"])
    result = api.query(data_input_dict)
    return result


def biz_create_and_view_charge(data_input_dict: dict):
    api = ChargeApi(secret_key=data_input_dict["secret_key"],
                    rsa_private=data_input_dict["rsa_private"],
                    request=data_input_dict["request"],
                    logger=data_input_dict["logger"])

    result_create = api.create(data_input_dict)
    charge_id = result_create["id"]
    result_view = api.view(charge_id)
    return result_create, result_view


