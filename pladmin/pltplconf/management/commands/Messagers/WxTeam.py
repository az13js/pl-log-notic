# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests
from django.conf import settings
import json

logger = logging.getLogger(__name__)

class WxTeam():
    def send(self, job, params):
        logger.debug("向企业微信群发送消息")
        if 0 == params["fail"]:
            messageText = "Hi，在最近的 " + str(params["total"]) + " 个请求中，成功的有 " + str(params["success"]) + " 个，失败的有 " + str(params["fail"]) + " 个。"
        else:
            messageText = "Hi，在最近的 " + str(params["total"]) + " 个请求中，成功的有 " + str(params["success"]) + " 个，失败的有 " + str(params["fail"]) + " 个。"
            messageText = messageText + "\n失败订单（最后10条内）为："
            for res in params["failOrderSn"]:
                messageText = messageText + "\n" + str(res)
            messageText = messageText + "\n失败返回结果（最后10条内）为："
            for res in params["failResults"]:
                messageText = messageText + "\n" + str(res)
            # str(res)而不是直接取res是因为出现这个报错：
            # TypeError: can only concatenate str (not "int") to str
            # 出错的位置是for res in params["failOrderSn"]那个地方
            # 估计是failOrderSn里面，有一个是用int类型而不是string类型作为了订单号
        messageText = messageText + "\n筛选条件：" + job.es_query
        data = {
            "msgtype": "text",
            "text": {
                "content": messageText
            }
        }
        logger.debug(messageText)
        requests.post(url = settings.MESSAGERS_CONFIG["WxTeam"], headers = {"Content-Type": "text/plain"}, json = data)
