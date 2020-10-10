# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests

logger = logging.getLogger(__name__)

class WXBot():
    def send(self, taskSetting, message):
        logger.debug("WXBot 向企业微信群发送消息")
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        logger.debug(message)
        requests.post(url = taskSetting.wx_bot_addr, headers = {"Content-Type": "text/plain"}, json = data)
