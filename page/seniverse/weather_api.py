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
        self.info("[%s] - 使用 URI %r " % (__name__, req_uri))

        req_method = self._get_config(self.__config, "NOW.METHOD")
        self.info("[%s] - 使用 METHOD %r " % (__name__, req_method))
        req_data = {
            self._get_config(self.__config, "NOW.PARAM.KEY"): self.api_key,
            self._get_config(self.__config, "NOW.PARAM.LOCATION"): data_dict.get("location"),
            self._get_config(self.__config, "NOW.PARAM.LANGUAGE"): data_dict.get("language"),
            self._get_config(self.__config, "NOW.PARAM.UNIT"): data_dict.get("unit")
        }
        self.info("[%s] - 开始使用 参数 %r " % (__name__, req_data))

        req_data = self._remove_none_param(req_data)
        self.info("[%s] - 完成去空 参数 %r " % (__name__, req_data))

        # 认证
        req_cookies = {}

        # 真正的发请求
        self._send(uri=req_uri,
                   method=req_method,
                   data_dict=req_data,
                   cookies=req_cookies
                   )
        self.info("[%s] - 发送请求，使用数据如下 %r " % (
            __name__,
            dict(uri=req_uri,
                 method=req_method,
                 data_dict=req_data,
                 cookies=req_cookies)))

        # 返回响应的结果
        resp_body_key_list = self._get_config(self.__config, "NOW.RESP.LIST.DATA_KEY")
        self.info("[%s] - 读取响应数据键 %r " % (__name__, resp_body_key_list))

        resp = self._parse(body_key_list=resp_body_key_list)
        self.info("[%s] - 收到 响应 %r " % (__name__, resp))

        # 处理list
        list_data_key = self._get_config(self.__config, "NOW.RESP.LIST.DATA_KEY")
        index = self._get_config(self.__config, "NOW.RESP.LIST.INDEX")
        sub_data_key_list = self._get_config(self.__config, "NOW.RESP.LIST.SUB_DATA_KEY")
        list_resp = self._parse_list(list_data_key=list_data_key,
                                     index=index,
                                     sub_data_key_list=sub_data_key_list)
        self.info("[%s] - 收到自定义解析响应 %r" % (__name__, list_resp))

        resp_result = self._merge_dict(resp, list_resp)
        self.info("[%s] - 合并之前的解析 %r 和刚刚的自定义解析 %r " % (
            __name__, resp, list_resp))

        return resp_result
