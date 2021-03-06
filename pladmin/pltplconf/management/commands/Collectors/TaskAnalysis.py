# -*- coding: utf8 -*-

"""示例用
在Linux系统中命令行方式使用代理服务，方式是设置环境变量：
http_poxy="http://user:password@www.example.cn:1000"
https_poxy="http://user:password@www.example.cn:1000"
"""
import json
import time
import logging
from datetime import timedelta, datetime, timezone
from pltplconf import api
from django.forms.models import model_to_dict
from pltplconf.management.commands.Collectors.ElasticsearchLongQuery import getEsObject, FakeRequest

logger = logging.getLogger(__name__)

class TaskAnalysis():
    def findLogs(self, job):
        logger.debug("查询命令是：" + job.task_setting.query_string)
        return api.doQuery(
            getEsObject(FakeRequest(job.task_setting)),
            job.task_setting.query_type,
            job.task_setting.query_string,
            datetime.now() - timedelta(seconds=job.delay_sec)
        )
