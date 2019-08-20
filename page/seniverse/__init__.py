from page import BaseApi

# 以下是测试用例使用的场景
from page.seniverse.life_api import LifeApi


def biz_view_life_suggestion(data_input_dict):
    """
    场景：查询生活指数的场景，事实上会调用 /v3/life/suggestion.json GET 请求
    :param data_input_dict: 字典，key 的列表至少包含
        key,
        location,
        language,
        request,
        logger
    :return: 字典 dict
        status_code
        接口的默认首层返回值 results
        自定义的 取 results 的第一个 元素
            location/name
            location/country
    """
    api = LifeApi(api_key=data_input_dict["api_key"],
                  request=data_input_dict["request"],
                  logger=data_input_dict["logger"])
    data_dict = dict(
        location=data_input_dict["location"],
        language=data_input_dict["language"]
    )
    result = api.suggest(data_dict)
    return result
