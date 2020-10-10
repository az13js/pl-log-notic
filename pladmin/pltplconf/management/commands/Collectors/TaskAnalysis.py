# -*- coding: utf8 -*-

"""示例用
在Linux系统中命令行方式使用代理服务，方式是设置环境变量：
http_poxy="http://user:password@www.example.cn:1000"
https_poxy="http://user:password@www.example.cn:1000"
"""
import json
import time
import logging
from pltplconf import api
from django.forms.models import model_to_dict

logger = logging.getLogger(__name__)

class TaskAnalysis():
    def findLogs(self, job):
        logger.debug("es查询采集部分，收到命令：" + job.task_setting.query_string)
        return api.doQuery(
            api.getEsObject(FakeRequest(job.task_setting)),
            job.task_setting.query_type,
            job.task_setting.query_string,
            round((time.time() - float(job.delay_sec)) * 1000)
        )

# 模拟request的属性
class FakeRequest():
    def __init__(self, taskSetting):
        self.body = json.dumps({"params": model_to_dict(taskSetting)}).encode()
