from base import read_yaml
from page.seniverse.api import SeniverseApi


class LifeApi(SeniverseApi):
    """
    标题： 生活类，生活模块的所有接口
    作者： 刘挺立
    日期： 20190820
    邮件： liutingli@ascents.work
    """
    __config = read_yaml(current=__file__, file_path="api.yml", key="LifeApi")

    def suggest(self, data_dict):
        """
        生活指数
        :param data_dict:
        :return:
        """
        req_uri = self._get_config(self.__config, "SUGGEST.URI")
        req_method = self._get_config(self.__config, "SUGGEST.METHOD")
        req_data = {
            self._get_config(self.__config, "SUGGEST.PARAM.KEY"): self.api_key,
            self._get_config(self.__config, "SUGGEST.PARAM.LOCATION"): data_dict.get("location"),
            self._get_config(self.__config, "SUGGEST.PARAM.LANGUAGE"): data_dict.get("language")
        }
        req_data = self._remove_none_param(req_data)
        # 认证
        req_cookies = {}

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   data_dict=req_data,
                   cookies=req_cookies
                   )
        # 返回响应的结果
        resp_body_key_list = self._get_config(self.__config, "SUGGEST.RESP.DATA_KEY")
        resp = self._parse(body_key_list=resp_body_key_list)

        # 处理 list
        list_data_key = self._get_config(self.__config, "SUGGEST.RESP.LIST.DATA_KEY")
        index = self._get_config(self.__config, "SUGGEST.RESP.LIST.INDEX")
        sub_data_key_list = self._get_config(self.__config, "SUGGEST.RESP.LIST.SUB_DATA_KEY")
        list_resp = self._parse_list(list_data_key=list_data_key,
                                     index=index, sub_data_key_list=sub_data_key_list)
        return self._merge_dict(resp, list_resp)
