# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.OrderSystemError import OrderSystemError as OrderSystemErrorController
import logging

logger = logging.getLogger(__name__)

class OrderSystemError():

    def __init__(self):
        self.OrderSystemErrorController = OrderSystemErrorController()

    def handle(self, job):
        logger.debug("OrderSystemError流水线，正在运作")
        if 3 == job.system_type:
            self.OrderSystemErrorController.errorSummary(job)






