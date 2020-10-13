# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.Task import Task as TaskController
import logging

logger = logging.getLogger(__name__)

class Task():

    def __init__(self):
        self.TaskController = TaskController()

    def handle(self, job):
        if 5 == job.system_type and 1 == job.task_setting.status:
            logger.debug("任务流水线正在处理，job=" + str(job) + ",关联的配置对象是，" + str(job.task_setting))
            self.TaskController.run(job)
