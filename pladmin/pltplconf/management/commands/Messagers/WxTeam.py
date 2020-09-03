# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests
from django.conf import settings
import json

logger = logging.getLogger(__name__)

class WxTeam():
    def send(self, params):
        logger.debug("向企业微信群发送消息")
        if 0 == params["fail"]:
            messageText = "Hi，在最近的 " + str(params["total"]) + " 笔订单中，成功的有 " + str(params["success"]) + " 笔，失败的有 " + str(params["fail"]) + " 笔。"
        else:
            messageText = "Hi，在最近的 " + str(params["total"]) + " 笔订单中，成功的有 " + str(params["success"]) + " 笔，失败的有 " + str(params["fail"]) + " 笔。\n部分失败返回结果为："
            for res in params["failResults"]:
                messageText = messageText + "\n" + res
        data = {
            "msgtype": "text",
            "text": {
                "content": messageText
            }
        }
        logger.debug(messageText)
        requests.post(url = settings.MESSAGERS_CONFIG["WxTeam"], headers = {"Content-Type": "text/plain"}, json = data)
