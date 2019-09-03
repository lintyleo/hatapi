__version__ = "2.0.2"
__author__ = "ArtLinty"
"""
# Usage：
# call build_request() for web api instance
"""
from urllib.parse import urlencode

from base.box import BoxRequest
from base.helper import CsvHelper, PathHelper, DbHelper, YamlHelper, DictHelper, read_txt_format
from base.infrastructure import Logger

"""
main portal, for web browser driver
"""

"""
main portal, for web api request
"""
__SUPPORT_SCHEMA_LIST = ["HTTPS", "HTTP"]


def build_request(
        schema: str,
        host: str,
        port=None):
    """
    get request for web api testing
    :param schema:
    :param port: 主机端口号
    :param host: API 网址的 主机部分
    :return: BoxRequest
    """

    if schema is not None and schema.upper().strip() in __SUPPORT_SCHEMA_LIST:
        if schema.upper().strip() == "HTTP":
            schema = BoxRequest.RequestType.HTTP
        elif schema.upper().strip() == "HTTPS":
            schema = BoxRequest.RequestType.HTTPS
        else:
            raise TypeError(
                "请传递一个合法的请求协议, 当前使用的 schema = %r"
                % schema
            )

    return BoxRequest(schema=schema, host=host, port=port)


"""
private method
"""


def build_logger(log_path):
    """
    build logger
    :param log_path:
    :return:
    """
    return Logger(
        log_path=log_path,
        call_path=__name__
    )


def encode_url(url: str, params: dict):
    """
    对 URL 进行编码
    :param url:
    :param params:
    :return:
    """
    return url, urlencode(params)


def read_txt(current, file_path):
    """
    读纯文本文件
    :param current:
    :param file_path:
    :return:
    """
    txt_file = PathHelper.get_actual_path_by_current_file(current, file_path)
    return read_txt_format(txt_file)


def read_csv(current, file_path):
    """
    读 CSV 文件，CSV 文件必须有标题
    :param current: 读 CSV 文件的绝对路径，直接填写 __file__ 就可以了
    :param file_path: CSV 文件相对当前的路径（是相对路径），当前文件通过相对路径访问 csv 所需要的路径字符串
    :return: list 列表，列表中的元素是 dict，dict 的 key 是 csv 的第一行的标题
    """
    csv_file = PathHelper.get_actual_path_by_current_file(current=current, file_path=file_path)
    return CsvHelper.read_for_parametrize(csv_file)


def read_yaml(current, file_path, key):
    """
    读 YAML 文件，YAML 文件必须有标题
    :param current: 读 YAML 文件的绝对路径，直接填写 __file__ 就可以了
    :param file_path: YAML 文件相对当前的路径（是相对路径）
    :param key: 读 YAML 文件中制定的 key
    :return: dict，dict 的内容是 YAML 对应的 key 的 value
    """
    yml_file = PathHelper.get_actual_path_by_current_file(current=current, file_path=file_path)
    return YamlHelper.get_config_as_dict(file=yml_file, key=key)


def read_json(current_file_path, json_to_current):
    """
    读 Json 文件，然后转化为 dict
    :param current_file_path:
    :param json_to_current:
    :return:
    """
    json_file = PathHelper.get_actual_path_by_current_file(current_file_path, json_to_current)
    return DictHelper.read_json_file_as_dict(json_file)


def parse_dict(dict_data: dict, data_key, index=None, sub_key=None):
    """
    解析 JSON
    :param dict_data: 被解析的 JSON 的字典格式
    :param data_key: 请用 "." 隔开路径
    :param index:
    :param sub_key:
    :return:
    """

    return DictHelper.parse_dict_value(
        json_dict=dict_data,
        data_key=data_key,
        index=index,
        sub_key=sub_key
    )


def random_string(length: int):
    """
    随机指定长度的字符串，包含大小写，数字，不包含特殊符号
    :param length: 长度
    :return: str
    """
    return helper.str_random(length=length)


def random_string_letters(length: int):
    """
    随机指定长度的字符串，只包含大小写，不包含数字，不包含特殊字符
    :param length: 长度
    :return: str
    """
    return helper.str_random(digits=False, length=length)


def random_string_with_punctuation(length: int):
    """
    随机指定长度的字符串，只包含大小写、数字和特殊字符
    :param length: 长度
    :return: str
    """
    return helper.str_random(punctuation=True, length=length)


def random_string_lower(length: int):
    """
    随机指定长度的字符串，只包含小写
    :param length: 长度
    :return: str
    """
    return helper.str_random(upper=False, digits=False, punctuation=False, length=length)


def random_string_digits(length: int):
    """
    随机指定长度的字符串，只包含数字
    :param length: 长度
    :return: str
    """
    return helper.str_random(upper=False, lower=False, punctuation=False, length=length)
