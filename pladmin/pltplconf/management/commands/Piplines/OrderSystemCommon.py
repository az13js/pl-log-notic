# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.OrderSystemCommon import OrderSystemCommon as OrderSystemCommonController
import logging

logger = logging.getLogger(__name__)

class OrderSystemCommon():

    def __init__(self):
        self.OrderSystemCommonController = OrderSystemCommonController()

    def handle(self, job):
        if 0 == job.system_type:
            logger.debug("OrderSystemCommonController流水线，正在处理，job=" + str(job))
            self.OrderSystemCommonController.successSummary(job)






