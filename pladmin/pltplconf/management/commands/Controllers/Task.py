# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.TaskAnalysis import TaskAnalysis
from pltplconf.management.commands.Parsers.TaskParser import TaskParser
from pltplconf.management.commands.Messagers.WXBot import WXBot
import logging
import json

logger = logging.getLogger(__name__)

class Task():

    def run(self, job):
        logger.debug("Task控制器开始执行，job id=" + str(job.id))
        queryLog = TaskAnalysis().findLogs(job)
        params = json.loads(queryLog)
        if "hits" in params and "hits" in params["hits"]:
            if len(params["hits"]["hits"]) >= job.task_setting.push_min:
                message = TaskParser().parse(job.task_setting, queryLog.encode("utf-8").decode("unicode_escape"))
                WXBot().send(job, message)
            else:
                logger.debug("达不到推送要求的下限，push_min=" + str(job.task_setting.push_min))
        else:
            logger.debug("找不到hits属性")
