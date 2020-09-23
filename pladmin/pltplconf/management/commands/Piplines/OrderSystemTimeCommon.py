# -*- coding: utf8 -*-

import logging
from pltplconf.management.commands.Controllers.OrderSystemTimeCommon import OrderSystemTimeCommon as OrderSystemTimeCommonController

logger = logging.getLogger(__name__)

class OrderSystemTimeCommon():

    def __init__(self):
        self.orderSystemTimeCommonController = OrderSystemTimeCommonController()

    def handle(self, job):
        if 4 == job.system_type:
            logger.debug("OrderSystemTimeCommon 匹配到JOB，正在执行: " + str(job))
            self.orderSystemTimeCommonController.executeTime(job)







