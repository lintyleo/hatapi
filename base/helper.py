__version__ = "2.0.2"
__author__ = "ArtLinty"

import csv
import json
import os

import pymysql
import yaml

_DEFAULT_ENCODING_UTF8 = "utf-8"
_CHARACTER_COMMA = ","
_CHARACTER_SLASH = "/"
_LEVEL_FROM_PROJECT_ROOT = "../"


class PathHelper(object):
    """
    路径处理
    """

    @staticmethod
    def get_actual_path_by_current_file(current, file_path):
        """
        获取绝对路径
        从项目根目录与执行文件的相对路径中获取绝对路径
        :param current: 当前文件的真实绝对路径
        :param file_path: 被访问文件与当前文件的相对路径
        :return: 路径
        """
        current_file_path = os.path.dirname(current)
        name_file_path = _parse_file_name(file_path)
        abspath = os.path.abspath(os.path.join(current_file_path, name_file_path))
        return abspath

    @staticmethod
    def get_actual_path_by_project_root(filename):
        """
        获取绝对路径
        从项目根目录与执行文件的相对路径中获取绝对路径
        :param filename: 被访问文件与当前项目的根目录的相对路径
        :return: 路径
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = _parse_file_name(filename)
        abspath = os.path.abspath(os.path.join(base_dir, _LEVEL_FROM_PROJECT_ROOT, filename))
        return abspath

    @staticmethod
    def file_is_exist(filename):
        """
        file is exist
        :param filename:
        :return:
        """
        return os.path.exists(filename)


class CsvHelper(object):

    @staticmethod
    def read_for_parametrize(f, encoding=_DEFAULT_ENCODING_UTF8):
        """
        读csv文件作为普通 Dict List
        :param f:
        :param encoding:
        :return:
        """
        data_ret = []
        with open(f, encoding=encoding, mode='r') as csv_file:
            csv_dict = csv.DictReader(csv_file)

            for row in csv_dict:
                row_dict = {}
                for key in row.keys():
                    value = row.get(key)
                    # 如果在 csv 中写的字符串是变成小写以后 是 "null", 就认定要给参数传递 None 值
                    if isinstance(value, str) and value.lower() == "null":
                        row_dict[key] = None
                    elif isinstance(value, str) and value.lower() in ["false", "true"]:
                        row_dict[key] = bool(row.get(key))

                    else:
                        row_dict[key] = parse_digit(row.get(key))
                data_ret.append(row_dict)

        return data_ret


class DbHelper(object):
    """
    MySQL 数据库帮助类
    """

    # 使用方法
    # 1. 实例化对象
    # 2. 查询，得到结果
    # 3. 关闭对象
    """
    db_helper = _DbHelper("localhost", 3306, 'root', '', 'tpshop2.0.5', "utf8")
    for i in range(10000):

        result = db_helper.execute("select * from tp_goods order by 1 desc limit 1000;")
        print("第%d次，结果是%r" % (i, result))

    db_helper.close()
    """

    connect = None

    def __init__(self, host, port, user, password, database, charset=_DEFAULT_ENCODING_UTF8):
        """
        构造方法
        :param host: 数据库的主机地址
        :param port: 数据库的端口号
        :param user: 用户名
        :param password: 密码
        :param database: 选择的数据库
        :param charset: 字符集
        """
        self.connect = pymysql.connect(host=host, port=port,
                                       user=user, password=password,
                                       db=database, charset=charset)

    @staticmethod
    def read_sql(file, encoding=_DEFAULT_ENCODING_UTF8):
        """
        从 文件中读取 SQL 脚本
        :param file: 文件名 + 文件路径
        :param encoding:
        :return:
        """
        sql_file = open(file, "r", encoding=encoding)
        sql = sql_file.read()
        sql_file.close()
        return sql

    def query(self, sql):
        """
        执行 SQL 脚本查询并返回结果
        :param sql: 需要查询的 SQL 语句
        :return: 字典类型
            data 是数据，本身也是个字典类型
            count 是行数
        """
        cursor = self.connect.cursor()

        row_count = cursor.execute(sql)
        rows_data = cursor.fetchall()
        result = {
            "count": row_count,
            "data": rows_data
        }

        cursor.close()
        return result

    def execute(self, sql):
        """
        执行 SQL 脚本查询并返回结果
        :param sql: 需要查询的 SQL 语句
        :return: 字典类型
            data 是数据，本身也是个字典类型
            count 是行数
        """
        cursor = self.connect.cursor()

        cursor.execute(sql)

        self.connect.commit()

        cursor.close()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.connect.close()


class YamlHelper(object):

    @staticmethod
    def get_config_as_dict(file, key=None):
        """
        获取所有配置 作为 Dict
        :param key: yaml 文件需要读取的  key
        :param file:
        :return:
        """
        with open(file, mode='r', encoding='utf8') as file_config:
            config_dict = yaml.load(file_config.read(), Loader=yaml.FullLoader)
            if key and config_dict and isinstance(config_dict, dict):
                return _get_dict_value(config_dict, key)

            return None

    @staticmethod
    def dict_to_yaml(yaml_dict: dict):
        """
        字典转 yaml 文件流
        :param yaml_dict:
        :return:
        """
        return yaml.dump(yaml_dict)


class JsonHelper(object):

    @staticmethod
    def parse_json_dict_value(json_dict, data_key, index=None, sub_key=None):
        """
        get json dict value
        :param json_dict:
        :param sub_key:
        :param data_key:
        :param index: 从 0 开始，默认值是 None
        :return:
        """

        ret_dict = _get_dict_value(json_dict, data_key)
        if index is None:
            index = -1
        if (index >= 0) and isinstance(ret_dict, list) and (len(ret_dict) > index):
            ret_dict = ret_dict[index]

        if sub_key is not None:
            ret_dict = _get_dict_value(ret_dict, sub_key)

        return ret_dict

    @staticmethod
    def convert_dict_to_json_str(json_dict):
        """
        转换 Python Dict 为 Json 格式
        :param json_dict:
        :return: str
        """
        if json_dict is not None and isinstance(json_dict, dict):
            return json.dumps(json_dict)

        return None

    @staticmethod
    def convert_json_str_to_dict(json_str_to_convert):
        """
        转 json 格式的 字符串 为 Python 字典 dict 类型
        建议使用 bejson.com 编写 json，然后 压缩成为字符串，复制到变量
        :param json_str_to_convert:
        :return: str
        """
        if json_str_to_convert is not None and isinstance(json_str_to_convert, str):
            return json.loads(json_str_to_convert)

        return None

    @staticmethod
    def read_json_file_as_dict(json_file):
        """
        读 json 文件，然后把文件中的字符串转换为 python 字典 dict 类型
        ：:param json_file:
        :return:
        """
        if json_file is not None and isinstance(json_file, str):
            with open(json_file, mode="r", encoding=_DEFAULT_ENCODING_UTF8) as f:
                json_string = f.read()
                return json.loads(json_string)

        return None


def read_txt_format(file_path):
    """
    读取 txt 格式的文本格式
    :param file_path:
    :return:
    """
    file = open(file_path, mode="r", encoding=_DEFAULT_ENCODING_UTF8)
    return file.read()


def parse_digit(string_to_parse):
    """
    根据输入的 字符串，判断
    - 字符串是否是数字
        - 如果字符串是数字，判断是否是整数
            - 如果是整数就返回整数
            - 否则返回小数
        - 如果字符串不是数字，返回字符串本身

    :param string_to_parse:
    :return:
    """
    if string_to_parse is not None and isinstance(string_to_parse, str):
        string_to_parse = string_to_parse.strip()
        if _is_decimal_string(string_to_parse):
            return _string_to_decimal(string_to_parse)

    return string_to_parse


def _is_decimal_string(num_string):
    """
    判断是否数值组成的字符串
    :param num_string:
    :return:
        如果 num_string 是空值，False
        如果是：纯数值组成的字符串， True
        否则：False
    """
    if not num_string:
        return False

    result = True
    # 开始判断：一个个字符来检查，只要不是
    # "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    # 循环 num_sting，一个个检查是不是个数字

    # 如果有大于1个 的 ".", 返回 False
    if num_string.count(".") > 1:
        return False

    # 如果第一位是 "-", 移除第一位，继续

    if len(num_string) > 0 and num_string[0] == "-":
        num_string = num_string[1:]

    # 如果有一位小数点，把小数点去掉
    if num_string.count(".") == 1:
        num_string = num_string.replace(".", "")

    # 遍历每一位，判断是否在 0-9
    for char in num_string:
        # 任意一位不是 0-9，就退出循环
        if not _is_digital(char):
            result = False
            break

    return result


def _is_digital(char):
    """
    判断 char 是否是以下任意一个：
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    :param char: 一位字符
    :return:
        如果是
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        任意一个，返回 True
        否则，False
    """
    # 判断 char 是否是 "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    # 的任意一个
    # if char not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):

    return "0" <= char <= "9"


def _string_to_decimal(num_string):
    """
    把代表数值的字符串转成实际的数值
    :param num_string:
    :return:
        _string_to_decimal("123"), 返回 123
        _string_to_decimal("123.098"), 返回 123.098
        _string_to_decimal("-123"), 返回 -123
        _string_to_decimal("-123.098"), 返回 -123.098

    """

    is_negative = False

    # 处理正负
    if num_string[0] == "-":
        is_negative = True
        num_string = num_string[1:]

    # 处理整数
    num_int = num_string.split(".")[0]
    result = _calc_string(num_int)

    # 判断小数位
    if "." in num_string:
        num_float = num_string.split(".")[1]
        # 处理小数
        result += _calc_string(num_float, True)

    # 处理负数运算
    if is_negative:
        result = -1 * result
    return result


def _calc_string(num_string, is_float=False):
    """
    处理数位
    :param num_string:
    :param is_float: 默认是 False，代表是处理整数部分
    :return:
        is_float 是 False：处理整数
            123 = 1 * 10^2 + 2 * 10^1 + 3 * 10^0
        is_float 是 True： 处理小数
            123 = 1 * 10^-1 + 2 * 10^-2 + 3 * 10^-3
    """
    if is_float:
        # 处理小数
        digit_length = -1
    else:
        digit_length = len(num_string) - 1

    re_value = 0
    for digit in num_string:
        digit_int = ord(digit) - 48
        re_value += digit_int * pow(10, digit_length)
        digit_length -= 1

    return re_value


def _parse_file_name(filename):
    """
    处理文件路径，如果是 "\"， 就改成 "/"，
    如果以 "/" 开头，要改成 "./" 开头
    :param filename:
    :return:
    """
    if filename is not None and isinstance(filename, str) and len(filename) > 0:
        filename = filename.replace("\\", "/")

        if filename[0] == "/":
            filename = ".%s" % filename

    return filename


def _get_dict_value(json_dict, data_key):
    """
    parse dict value
    :param json_dict:
    :param data_key:
    :return:
    """
    keys = []
    if _CHARACTER_SLASH in data_key:
        keys = data_key.split(_CHARACTER_SLASH)
    else:
        keys.append(data_key.strip())

    if isinstance(json_dict, dict):
        for k in keys:
            k = k.strip()
            if k in json_dict.keys():
                json_dict = json_dict[k]
            else:
                json_dict = None
                break

    return json_dict
