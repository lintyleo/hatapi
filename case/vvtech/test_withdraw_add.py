import allure
import pytest

from base import read_csv, read_yaml, parse_dict
from case import BaseTest
from page.vvtech import biz_add_withdraw


class TestWithdrawAdd(BaseTest):
    """
    标题： 在支付对象接口，使用合法有效的数据请求 创建支付的接口，创建成功
    作者： 刘挺立
    时间： 20190813
    邮件： liutingli@ascents.work
    """
    __test = dict(
        collection=read_csv(current=__file__, file_path="test_withdraw_add.csv"),
        config=read_yaml(current=__file__, file_path="../../config/env_active.yml", key="vvtech"),
        title="在支付对象接口，使用合法有效的数据请求，创建支付的接口，创建成功",
        case="https://dwz.cn/GUIf2ZeN",
        feature="取款接口",
        story="取款对象的创建",
        tag=("api", "vvtech", "add", "valid"),
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
        self.init_request(
            schema=parse_dict(dict_data=self.__test, data_key="config.schema"),
            host=parse_dict(dict_data=self.__test, data_key="config.host")
        )
        # 是 yield 关键字，代表执行 test_ 开头的方法的具体内容
        self.info("[%s] - 完成测试的前置条件 set_up！ " % __name__)
        yield

        # 最后是清理操作，在 yield 之后
        self.wait()
        self.info("[%s] - 完成测试的清理操作 tear_down！ " % __name__)

    @allure.feature(__test.get("feature"))
    @allure.story(__test.get("story"))
    @allure.tag(*__test.get("tag"))
    @allure.severity(__test.get("severity"))
    @allure.testcase(url=__test.get("case"))
    @allure.title(__test.get("title"))
    @pytest.mark.parametrize("data", __test.get("collection"))
    def test_charges_create(self, data):
        """
        执行测试的具体步骤
        :param data: 通过读取 __test_data_collection 得到一条 test_data
        :return: None
        """
        self.info("[%s] - 开始执行测试，使用数据：%r！ " % (__name__, data))
        # 准备数据 从 test_data 取数据

        data_input_dict = dict(
            vv_vv_signature=data.get("签名"),
            vv_time=data.get("时间戳"),
            app_secret=data.get("密钥"),
            client_id=data.get("客户编号"),
            password=data.get("密码"),
            is_android=data.get("平台"),
            mobile=data.get("手机号"),
            version=data.get("版本"),
            amount=data.get("金额"),
            bank_card_id=data.get("卡号"),
            request=self.request,
            logger=self.logger
        )

        # 调用业务，使用上面准备的数据
        self.info("[%s] - 开始调用业务，使用数据 data_input_dict：%r！ " % (__name__, data_input_dict))
        resp, resp2 = biz_add_withdraw(data_input_dict)

        # 对比结果，使用 test_data 取到的期望，和上一步执行得到的结果进行对比
        self.info("[%s] - 开始进行断言，使用数据 resp：%r！ " % (__name__, resp))
        assert self.assert_equal(expected=data.get("期望状态码"), actual=resp.get("status_code"))
        assert self.assert_equal(expected=data.get("期望状态码"), actual=resp2.get("status_code"))
        assert self.assert_int_equal(expected=data.get("期望flag"), actual=resp2.get("flag"))

        self.info("[%s] - 结束执行测试，使用数据：%r！ " % (__name__, data))
