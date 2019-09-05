from page.vvtech.withdraw_api import WithdrawApi


def biz_add_withdraw(data_input_dict: dict):
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
    api = WithdrawApi(
        request=data_input_dict["request"],
        logger=data_input_dict["logger"]
    )

    result = api.login(data_input_dict)
    data_input_dict["token"] = result["data.token"]
    result2 = api.add(data_input_dict)

    return result, result2
