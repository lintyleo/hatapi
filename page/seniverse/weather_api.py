from base import read_yaml
from page.seniverse.api import SeniverseApi


class WeatherApi(SeniverseApi):
    """
    标题： 天气类，天气模块的所有接口
    作者： 梁静
    日期： 190826
    邮件： liangjing@ascents.work
    """
    __config = read_yaml(current=__file__, file_path="api.yml", key="WeatherApi")

    def now(self, data_dict):
        """
        当前天气
        :param self:
        :param data_dict:
        :return:
        """
        req_uri = self._get_config(self.__config, "NOW.URI")
        req_method = self._get_config(self.__config, "NOW.METHOD")
        req_data = {
            self._get_config(self.__config, "NOW.PARAM.KEY"): self.api_key,
            self._get_config(self.__config, "NOW.PARAM.LOCATION"): data_dict.get("location"),
            self._get_config(self.__config, "NOW.PARAM.LANGUAGE"): data_dict.get("language"),
            self._get_config(self.__config, "NOW.PARAM.UNIT"): data_dict.get("unit")
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
        resp_body_key_list = self._get_config(self.__config, "NOW.RESP.LIST.DATA_KEY")
        resp = self._parse(body_key_list=resp_body_key_list)

        # 处理list
        list_data_key = self._get_config(self.__config, "NOW.RESP.LIST.DATA_KEY")
        index = self._get_config(self.__config, "NOW.RESP.LIST.INDEX")
        sub_data_key_list = self._get_config(self.__config, "NOW.RESP.LIST.SUB_DATA_KEY")
        list_resp = self._parse_list(list_data_key=list_data_key,
                                     index=index,
                                     sub_data_key_list=sub_data_key_list)
        return self._merge_resp(resp, list_resp)
