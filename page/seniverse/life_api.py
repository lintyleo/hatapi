from page.seniverse import SeniverseApi


class LifeApi(SeniverseApi):

    def suggest(self, data_dict):
        req_uri = "/v1/charges"
        # 方法
        req_method = "get"
        # 参数
        req_data = {
            "key": self.api_key,
            "location": data_dict["location"],
            "language": data_dict["language"]
        }
        # 认证
        req_auth = {}
        # cookies
        req_cookies = {}
        # headers
        req_headers = {}
        # 真正的发请求
        self.send(uri=req_uri,
                  method=req_method,
                  params=req_data,
                  auth=req_auth,
                  cookies=req_cookies,
                  headers=req_headers)
        # 返回响应的结果
        resp_body_key_list = ["id", "object", "created", "livemode"]
        return self.parse(body_key_list=resp_body_key_list)
