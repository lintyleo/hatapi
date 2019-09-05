from base import read_yaml
from page.vvtech.api import VvtechApi


class WithdrawApi(VvtechApi):
    """
    标题： 业务类，普通支付模块的所有接口
    作者： 刘挺立
    日期： 20190819
    邮件： liutingli@ascents.work
    """
    __config = read_yaml(current=__file__, file_path="api.yml", key="WithdrawApi")

    def add(self, data_dict: dict):
        """
        真实的调用 POST /v1/charges 接口
        :param data_dict:  dict
            需要的key
                order_no
                amount,
                channel,
                currency,
                subject,
                body,
                description,
                extra: 需要是个字典，根据 channel
                app: 需要是个字典，{"id": your_app_id}
        :return:
        """
        # 格式化处理请求的数据
        # URI
        req_uri = self._get_config(self.__config, "ADD.URI")
        req_method = self._get_config(self.__config, "ADD.METHOD")
        token = data_dict.get("token")
        if token is None or token == "":
            token = self.token

        req_data = {
            self._get_config(self.__config, "ADD.PARAM.PASSWORD"): data_dict.get("password"),
            self._get_config(self.__config, "ADD.PARAM.BANK_CARD_ID"): data_dict.get("bank_card_id"),
            self._get_config(self.__config, "ADD.PARAM.AMOUNT"): data_dict.get("amount"),
            self._get_config(self.__config, "ADD.PARAM.APP_SECRET"): data_dict.get("app_secret")
        }
        req_data = self._remove_none_param(req_data)
        # 认证
        req_body = self._get_body_for_signature(token=token, request_body=req_data)

        req_data.update(req_body)
        req_data[self._get_config(self.__config, "ADD.PARAM.TOKEN")] = token

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   data_dict=req_data)
        # 返回响应的结果
        resp_body_key_list = self._get_config(self.__config, "ADD.RESP.DATA_KEY")
        return self._parse(body_key_list=resp_body_key_list)
