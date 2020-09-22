# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests
from django.conf import settings
import json

logger = logging.getLogger(__name__)

class WxTeamXLog():
    def send(self, job, params):
        logger.debug("WxTeamXLog向企业微信群发送消息")
        messageText = "【" + params["job_name"] + "】\nHi，查询到 " + str(params["total"]) + " 个。"
        display = 0
        for text in params["errorMessages"]:
            display = display + 1
            if display > 10:
                break
            messageText = messageText + text + "\n\n"
        data = {
            "msgtype": "text",
            "text": {
                "content": messageText
            }
        }
        logger.debug(messageText)
        requests.post(url = settings.MESSAGERS_CONFIG["WxTeam"], headers = {"Content-Type": "text/plain"}, json = data)
