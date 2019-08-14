def biz_create_charge(data_input_dict: dict):
    """
    场景：创建支付对象的场景，事实上会调用 /v1/charge POST 请求
    :param data_input_dict: dict 必须是字典，至少有以下的 key
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
    return []
