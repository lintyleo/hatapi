import allure
import pytest

from base import read_csv, read_yaml, read_txt
from case import BaseTest
from page.pingxx import biz_create_charge


class TestChargesCreate(BaseTest):
    """
    标题： 在支付对象接口，使用合法有效的数据请求 创建支付的接口，创建成功
    作者： 刘挺立
    时间： 20190813
    邮件： liutingli@ascents.work
    """
    __test = dict(
        collection=read_csv(current=__file__, file_path="test_charges_create.csv"),
        host=read_yaml(current=__file__, file_path="../../config/env_active.yml", key="pingxx/host"),
        title="在支付对象接口，使用合法有效的数据请求，创建支付的接口，创建成功",
        case=dict(
            url="https://dwz.cn/GUIf2ZeN"
        ),
        feature="支付接口",
        story="支付对象的创建",
        tag=("api", "pingxx", "create", "valid"),
        severity=allure.severity_level.CRITICAL
    )

    @pytest.fixture(autouse=True)
    def prepare(self):
        """
        测试执行使用的测试固件，包含前置条件和清理操作
        :return: None
        """
        # 首先是前置条件，在 yield 之前
        # 准备日志文件，就可以记录整个测试
        self.init_logger(__name__)
        # 准备请求对象，就可以传递请求给业务，也可以对请求进行抓包截图
        self.init_request(schema="HTTPS", host=self.__test["host"])
        # 是 yield 关键字，代表执行 test_ 开头的方法的具体内容
        self.info("[%s] - 完成测试的前置条件 set_up！ " % __name__)
        yield

        # 最后是清理操作，在 yield 之后
        self.wait()
        self.info("[%s] - 完成测试的清理操作 tear_down！ " % __name__)

    @allure.feature(__test["feature"])
    @allure.story(__test["story"])
    @allure.tag(*__test["tag"])
    @allure.severity(__test["severity"])
    @allure.testcase(url=__test["case"]["url"])
    @allure.title(__test["title"])
    @pytest.mark.parametrize("data", __test["collection"])
    def test_charges_create(self, data):
        """
        执行测试的具体步骤
        :param data: 通过读取 __test_data_collection 得到一条 test_data
        :return: None
        """
        self.info("[%s] - 开始执行测试，使用数据：%r！ " % (__name__, data))
        # 准备数据 从 test_data 取数据
        rsa_raw = data["RSA私钥"]
        if rsa_raw is not None and rsa_raw != "":
            rsa_private = read_txt(current=__file__, file_path=rsa_raw)
        else:
            rsa_private = None
        data_input_dict = dict(
            order_no=data["订单编号"],
            amount=data["金额"],
            channel=data["渠道"],
            currency=data["货币"],
            subject=data["主题"],
            body=data["正文"],
            description=data["描述"],
            extra=read_yaml(
                current=__file__,
                file_path=data["extra"],
                key="%s/data/extra" % data["数据编号"]),
            app=dict(id=data["app"]),
            client_ip=data["client_ip"],
            secret_key=data["密钥"],
            rsa_private=rsa_private,
            request=self.request,
            logger=self.logger
        )

        # 调用业务，使用上面准备的数据
        self.info("[%s] - 开始调用业务，使用数据 data_input_dict：%r！ " % (__name__, data_input_dict))
        resp = biz_create_charge(data_input_dict)

        # 对比结果，使用 test_data 取到的期望，和上一步执行得到的结果进行对比
        self.info("[%s] - 开始进行断言，使用数据 resp：%r！ " % (__name__, resp))
        assert self.assert_equal(expected=data["期望状态码"], actual=resp["status_code"])
        assert self.assert_equal(expected=data["期望object"], actual=resp["object"])
        assert self.assert_equal(expected=bool(data["期望paid"]), actual=resp["paid"])
        assert self.assert_equal(expected=data["渠道"], actual=resp["channel"])
        assert self.assert_equal(expected=data["金额"], actual=resp["amount"])

        self.info("[%s] - 结束执行测试，使用数据：%r！ " % (__name__, data))
