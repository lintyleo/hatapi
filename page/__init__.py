class BaseApi(object):

    def _send(self, uri: str,
              method: str,
              params=None,
              body=None,
              auth=None,
              cookies=None,
              headers=None,
              is_json_content=True):
        # TODO: 在业务的基类中，定义的发请求的方法
        self.info("")
        pass

    def _parse(self, body_key_list=None):
        """
        解析 send 的结果
        :param body_key_list: 需要解析的响应正文中的 key 的列表
        :return:
        """
        # TODO: 在业务的基类中，定义的收响应的方法
        self.info("")
        pass

    def _remove_none_param(self, param: dict):
        """
        移除掉参数字典中，值是 None 的元素，保证做到参数不传
        :param param:
        :return:
        """
        # TODO: 在业务的基类中，定义的移除None参数的方法
        self.info("")
        pass

    def info(self, msg):
        """
        记录日志
        :param msg:
        :return:
        """