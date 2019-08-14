from page import BaseApi


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
    # TODO: 场景方法，给测试用例使用，查询生活指数
    return {}


class SeniverseApi(BaseApi):
    __api_key = None

    def __init__(self, api_key):
        self.__api_key = api_key

    @property
    def api_key(self):
        return self.__api_key
