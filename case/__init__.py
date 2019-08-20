__version__ = "2.0.2"
__author__ = "ArtLinty"

import time

import allure

from base import build_request, build_logger, BoxRequest, PathHelper, Logger, YamlHelper, JsonHelper, parse_json
from base.helper import parse_digit


class BaseTest(object):
    """
    描述： 所有测试用例脚本的基类，原则上每一个测试用例都要继承
    作者： 刘挺立
    时间： 20190813
    邮件： liutingli@ascents.work
    """
    __logger = None
    __request = None

    def info(self, msg: str):
        """
        记录日志，记录测试日志
        :param msg: 字符串，需要记录的内容，建议把当前操作的数据写进来
        :return: None
        """
        if self.logger is not None and isinstance(self.logger, Logger):
            self.logger.info(msg)

    def init_logger(self, file_name: str):
        """
        初始化测试用例的日志文件，传递给 self._logger
        :param file_name: 在用例中，只需要传递 __name__ （固定用法，请勿改）
        :return: None
        """
        self.info("[%s] - 系统初始化日志，文件名：%s" % (__name__, file_name))

        if file_name is not None:
            if ".log" in file_name.strip():
                file_name = file_name.strip().replace(".log", "")

            file_name = "report/log/%s_%s.log" % (file_name, self.current_time_string)
        log_path = PathHelper.get_actual_path_by_project_root(file_name)
        self.__logger = build_logger(log_path=log_path)

    def init_request(self, schema: str, host: str, port=None):
        """
        初始化测试用例的请求对象，传递给 self._request
        :param schema: 协议，http 或者 https，忽略大小写
        :param host: 主机，ip 地址，或者 域名，或者 localhost 等主机名，忽略大小写
        :param port: 数字，整型，默认可以不传，如果不传，就使用 schema 的默认端口
            http： 默认 80
            https： 默认 443
        :return: None
        """
        self.info("[%s] - 系统初始化请求，请求数据：%r" % (__name__, {"schema": schema, "host": host, "port": port}))
        self.__request = build_request(schema=schema, host=host, port=port)

    def wait(self, seconds=5):
        """
        让 python 等待，默认 5 秒钟
        :param seconds: int， 大于 0
        :return:
        """
        if not isinstance(seconds, int) or seconds <= 0:
            seconds = 5

        self.info("[%s] - 系统等待执行 %d 秒" % (__name__, seconds))
        time.sleep(seconds)

    @allure.step
    def capture(self, title=None):
        """
        抓包 HTTP/HTTPS 请求和响应，并且记录在 allure 报告中
        :return: None
        """
        if title is None or title == "":
            title = self.current_timestamp
        if self.request and isinstance(self.request, BoxRequest):
            json = self.request.json_format_string
            allure.attach(json, name="json_dict_%s" % title, attachment_type=allure.attachment_type.JSON)

            response = self.dict_to_yaml(self.request.response_dict)
            allure.attach(response, name="full_response_%s" % title, attachment_type=allure.attachment_type.YAML)

            self.info("[%s] - 系统进行抓包，响应：%r，JSON：%r " % (__name__, response, json))

    def assert_in(self, expected, actual):
        """
        assert in, expected in actual
        :param expected:
        :param actual:
        :return:
            例如
                "胡艳" in "胡晓艳"  fail
                "胡" in "胡晓艳"  success
        """
        result = expected in actual
        log_msg = "[%s] - 系统进行断言 assert_in：{%r} in {%r} 的结果是 {%r}！" % (__name__, expected, actual, result)

        self.info(log_msg)
        # 如果执行断言失败，就抓包
        if not result:
            self.capture(log_msg[0: 20])
        return result

    def assert_equal(self, expected, actual):
        """
        assert equal
        :param expected:
        :param actual:
        :return: boolean， True 或者 False，让用例 通过 assert 使用
            :usage
                assert self.assert_equal(expected=xx, actual=yy)
            类型要一致
            例如
                "1" == 1  fail
                1 == 1 success
                str, int, float, boolean( True, False)...
                object 类型不可以相等
                    api1 = NspUserApi()
                    api2 = NspUserApi()
                    api1 == api2  fail
        """
        result = expected == actual
        log_msg = "[%s] - 系统进行断言 assert_equal：{%r} == {%r} 的结果是 {%r}！" % (
            __name__, expected, actual, result)

        self.info(log_msg)
        # 如果执行断言失败，就抓包
        if not result:
            self.capture(log_msg[0: 20])
        return result

    def assert_int_equal(self, expected, actual):
        """
        assert int equal, 忽略字符串和数字之间的差异
        :param expected:
        :param actual:
        :return:
            例如
                assert_int_equal(1, "1") success
                assert_int_equal(1.0, "1")  success
                assert_int_equal(-1.0, "-1")  success
                assert_int_equal(-1.0, "-1.0")  success
                assert_int_equal(-1, "-1.0")  success
        """
        result = False

        expected = self.str_to_decimal(expected, digits=0)
        actual = self.str_to_decimal(actual, digits=0)

        if expected is not None and actual is not None:
            result = expected == actual

        log_msg = "[%s] - 系统进行断言 assert_int_equal：{%r} == {%r} 的结果是 {%r}！" % (
            __name__, expected, actual, result)

        self.info(log_msg)
        # 如果执行断言失败，就抓包
        if not result:
            self.capture(log_msg[0: 20])
        return result

    def assert_decimal_equal(self, expected, actual, digits=2):
        """
        assert int equal, 忽略字符串和数值的差别
        :param digits: 小数位数
        :param expected:
        :param actual:
        :return:
            例子
                assert_decimal_equal("123.88", 123.88, 2) success
                assert_decimal_equal("123.88", 123.88, 1) success
                assert_decimal_equal("123.88", 123.89, 1) success
                assert_decimal_equal("123.88", 123.89, 2) fail
        """
        result = False

        expected = self.str_to_decimal(expected, digits)
        actual = self.str_to_decimal(actual, digits)

        if expected is not None and actual is not None:
            result = expected == actual

        log_msg = "[%s] - 系统进行断言 assert_decimal_equal：小数位{%r}, {%r} == {%r} 的结果是 {%r}！" \
                  % (__name__, digits, expected, actual, result)

        self.info(log_msg)
        # 如果执行断言失败，就抓包
        if not result:
            self.capture(log_msg[0: 20])
        return result

    def assert_dict_equal(self, expected, actual, data_key, index=None, sub_key=None):
        """
        断言 字典是否相等
        :param expected: 期望的结果 dict 格式
        :param actual: 实际的结果 dict 格式
        :param data_key: data key
        :param index: 下标，默认为 None
        :param sub_key: 子 data key，默认为 None
        :return:
        """
        result = False
        expected_value = parse_json(expected, data_key, index, sub_key)
        actual_value = parse_json(actual, data_key, index, sub_key)

        if expected_value is not None and actual_value is not None:
            result = expected_value == actual_value

        log_msg = "[%s] - 系统进行断言 assert_dict_equal： {%r} == {%r}, data_key=%s, index=%r, sub_key=%s 的结果是 {%r}！" \
                  % (__name__, expected, actual, data_key, index, sub_key, result)

        self.info(log_msg)
        # 如果执行断言失败，就抓包
        if not result:
            self.capture(log_msg[0: 20])
        return result

    def str_to_decimal(self, digit_str, digits=None):
        """
        转变 字符串（数字组成的字符串）为数字
        :param digits: 数值的小数位数，默认是 None
        :param digit_str: 数字组成的字符串
            规则：
                接受整型 "123"
                接受负数 "-123"
                接受小数 "-123.88"， "123.88"

        :return:
            如果 digit_str 是字符串 str 格式，就转化
            否则，返回 原样的值
        """
        self.info("[system] - [%s] str_to_decimal: %s" % (__name__, digit_str))
        ret_decimal = digit_str
        if digit_str is not None and isinstance(digit_str, str):
            ret_decimal = parse_digit(digit_str)
        if digits is not None and isinstance(ret_decimal, float) and isinstance(digits, int):
            ret_decimal = round(ret_decimal, digits)
        return ret_decimal

    def json_to_dict(self, json_str_to_convert):
        """
        转 json 格式的 字符串 为 Python 字典 dict 类型
        建议使用 bejson.com 编写 json，然后 压缩成为字符串，复制到变量
        :param json_str_to_convert:
        :return: dict
        """
        self.info("[system] - [%s] json_to_dict: %s" % (__name__, json_str_to_convert))
        if json_str_to_convert is not None and isinstance(json_str_to_convert, str):
            return JsonHelper.convert_json_str_to_dict(json_str_to_convert)

        return None

    def dict_to_yaml(self, dict_to_convert):
        """
        字典转 yaml 格式
        :param dict_to_convert:
        :return:
        """
        self.info("[system] - [%s] dict_to_yaml: %s" % (__name__, dict_to_convert))
        if dict_to_convert is not None and isinstance(dict_to_convert, dict):
            return YamlHelper.dict_to_yaml(dict_to_convert)

        return None

    @property
    def request(self):
        """
        请求对象，给业务使用，让他使用这个对象发请求
        :return:
        """
        return self.__request

    @property
    def logger(self):
        """
        日志对象，给业务使用，让他使用这个对象写日志，把他做的事情记录在里面
        :return:
        """
        return self.__logger

    @property
    def current_time_string(self):
        """
        当前时间的字符串格式
        :return:
        """
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

    @property
    def current_timestamp(self):
        """
        当前时间戳
        :return: 精确到整数
        """
        return round(time.time(), 0)
