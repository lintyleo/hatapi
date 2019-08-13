import allure
import pytest

from base import read_csv, read_yaml
from case import BaseCase
from page.pingxx import biz_create_charge


class ChargeCreateTest(BaseCase):
    """
    标题： 在支付对象接口，使用合法有效的数据请求 创建支付的接口，创建成功
    作者： 刘挺立
    时间： 20190813
    邮件： liutingli@ascents.work
    """
    __test_data_collection = read_csv(current=__file__, file_path="charge_create_test.csv")

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
        self.init_request(schema="HTTPS", host="api.pingxx.com")
        # 是 yield 关键字，代表执行 test_ 开头的方法的具体内容
        self.info("[%s] - 完成测试的前置条件 set_up！ " % __name__)
        yield

        # 最后是清理操作，在 yield 之后
        self.wait()
        self.info("[%s] - 完成测试的清理操作 tear_down！ " % __name__)

    @allure.feature("支付接口")
    @allure.story("支付对象的创建")
    @allure.tag("api", "pingxx", "create", "valid")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase(url="https://dwz.cn/GUIf2ZeN", name="在支付对象接口，使用合法有效的数据请求，创建支付的接口，创建成功")
    @pytest.mark.parametrize("test_data", __test_data_collection)
    def test_charge_create(self, test_data):
        """
        执行测试的具体步骤
        :param test_data: 通过读取 __test_data_collection 得到一条 test_data
        :return: None
        """
        self.info("[%s] - 开始执行测试，使用数据：%r！ " % (__name__, test_data))
        # 准备数据 从 test_data 取数据
        data_input_dict = dict(
            order_no=test_data["订单编号"],
            amount=test_data["金额"],
            channel=test_data["渠道"],
            currency=test_data["货币"],
            subject=test_data["主题"],
            body=test_data["正文"],
            description=test_data["描述"],
            extra=read_yaml(
                current=__file__,
                file_path=test_data["extra"],
                key="%s/data/extra" % test_data["数据编号"]),
            app=dict(id=test_data["app"]),
            ip=test_data["ip"],
            secret_key=test_data["密钥"],
            request=self.request,
            logger=self.logger
        )

        # 调用业务，使用上面准备的数据
        self.info("[%s] - 开始调用业务，使用数据 data_input_dict：%r！ " % (__name__, data_input_dict))
        resp = biz_create_charge(data_input_dict)

        # 对比结果，使用 test_data 取到的期望，和上一步执行得到的结果进行对比
        self.info("[%s] - 开始进行断言，使用数据 resp：%r！ " % (__name__, resp))
        assert self.assert_equal(expected=test_data["期望状态码"], actual=resp["status_code"])
        assert self.assert_equal(expected=test_data["期望object"], actual=resp["object"])
        assert self.assert_equal(expected=test_data["期望paid"], actual=resp["paid"])
        assert self.assert_equal(expected=test_data["channel"], actual=resp["channel"])
        assert self.assert_equal(expected=test_data["amount"], actual=resp["amount"])

        self.info("[%s] - 结束执行测试，使用数据：%r！ " % (__name__, test_data))
