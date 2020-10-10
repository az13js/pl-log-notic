# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.TaskAnalysis import TaskAnalysis
from pltplconf.management.commands.Parsers.TaskParser import TaskParser
from pltplconf.management.commands.Messagers.WXBot import WXBot
import logging
import json

logger = logging.getLogger(__name__)

class Task():

    def run(self, job):
        logger.debug("Task控制器开始执行，JOB=" + str(job))
        queryLog = TaskAnalysis().findLogs(job)
        params = json.loads(queryLog)
        if "responses" in params and "hits" in params["responses"][0] and "total" in params["responses"][0]["hits"] and params["responses"][0]["hits"]["total"] >= job.task_setting.push_min:
            message = TaskParser().parse(job.task_setting, queryLog)
            WXBot().send(job.task_setting, message)
