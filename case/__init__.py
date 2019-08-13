import time

import allure


class BaseCase(object):
    """
    描述： 所有测试用例脚本的基类，原则上每一个测试用例都要继承
    作者： 刘挺立
    时间： 20190813
    邮件： liutingli@ascents.work
    """
    _logger = None
    _request = None

    def info(self, msg: str):
        """
        记录日志，记录测试日志
        :param msg: 字符串，需要记录的内容，建议把当前操作的数据写进来
        :return: None
        """
        # TODO: 记录日志

    def init_logger(self, file_name):
        """
        初始化测试用例的日志文件，传递给 self._logger
        :param file_name: 在用例中，只需要传递 __name__ （固定用法，请勿改）
        :return: None
        """
        self.info("[%s] - 系统初始化日志，文件名：%s" % (__name__, file_name))
        # TODO: 初始化 日志对象

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
        # TODO: 初始化 请求对象

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
    def capture(self):
        """
        抓包 HTTP/HTTPS 请求和响应，并且记录在 allure 报告中
        :return: None
        """
        self.info("[%s] - 系统进行抓包，请求：%r，响应：%r，JSON：%r " % (__name__, "", "", ""))
        # TODO: 抓包请求的数据

    def assert_equal(self, expected, actual):
        """
        断言相等
        :param expected: 期望数据
        :param actual:  实际数据
        :return:  boolean， True 或者 False，让用例 通过 assert 使用
            :usage
                assert self.assert_equal(expected=xx, actual=yy)
        """
        result = expected == actual
        self.info("[%s] - 系统进行断言，结果：失败 %s，其中 %r != %r " % (__name__, result, expected, actual))

        # 如果执行断言失败，就抓包
        if not result:
            self.capture()

        return result

    @property
    def request(self):
        """
        请求对象，给业务使用，让他使用这个对象发请求
        :return:
        """
        return self._request

    @property
    def logger(self):
        """
        日志对象，给业务使用，让他使用这个对象写日志，把他做的事情记录在里面
        :return:
        """
        return self._logger
