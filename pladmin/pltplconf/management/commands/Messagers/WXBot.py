# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests
from django.utils import timezone
from datetime import timedelta
from pltplconf.models import PlPushLog

logger = logging.getLogger(__name__)

class WXBot():
    def send(self, job, message):
        taskSetting = job.task_setting
        # 没达到推送频率限制的可以推送：
        if PlPushLog.objects.filter(job_pri_key=job.id, push_time__gte=timezone.now() - timedelta(hours=1)).count() < taskSetting.max_per_hour:
            pushMessage = message
            if len(pushMessage) > 1024:
                pushMessage = pushMessage[0:1024]
            logger.debug("实际推送的消息：\n" + pushMessage)
            data = {
                "msgtype": "text",
                "text": {
                    "content": pushMessage
                }
            }
            requests.post(url = taskSetting.wx_bot_addr, headers = {"Content-Type": "text/plain"}, json = data)
            PlPushLog(push_time = timezone.now(), job_pri_key = job.id).save()
        else:
            logger.debug("已达到推送频率的极限，不会推送。")
