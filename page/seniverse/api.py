from page import BaseApi


class SeniverseApi(BaseApi):
    __api_key = None

    def __init__(self, request, logger, api_key: str):
        """
        构造 PingxxApi 的方法
        :param secret_key: 开发密钥
        :param rsa_private:  RSA商户私钥（需要整个字符串文本）
        """
        # 调用父类，完成父类的构造方法
        super().__init__(request=request, logger=logger)
        self.__api_key = api_key

    @property
    def api_key(self):
        """
        认证【属性】
        :return:
        """
        return self.__api_key
