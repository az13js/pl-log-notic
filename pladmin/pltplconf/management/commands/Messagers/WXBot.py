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
        if PlPushLog.objects.filter(job_pri_key=job.id, push_time__gte=timezone.now() - timedelta(hours=1)).count() < taskSetting.max_per_hour:
            logger.debug("WXBot 向企业微信群发送消息")
            data = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            logger.debug(message)
            requests.post(url = taskSetting.wx_bot_addr, headers = {"Content-Type": "text/plain"}, json = data)
            PlPushLog(push_time = timezone.now(), job_pri_key = job.id).save()
