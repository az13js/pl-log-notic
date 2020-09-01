# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests

logger = logging.getLogger(__name__)

class WxTeam():
    wxAddress = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0000000000000000000"

    def send(self, params):
        logger.debug("向企业微信群发送消息")
        data = {
            "msgtype": "text",
            "text": {
                "content": "Hi，在最近的 " + str(params["total"]) + " 笔订单中，成功的有 " + str(params["success"]) + " 笔，失败的有 " + str(params["fail"]) + " 笔。"
            }
        }
        requests.post(url = self.wxAddress, headers = {"Content-Type": "text/plain"}, json = data)
