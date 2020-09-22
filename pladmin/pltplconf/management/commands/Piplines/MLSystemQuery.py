# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.MLSystemQuery import MLSystemQuery as MLSystemQueryController
import logging

logger = logging.getLogger(__name__)

class MLSystemQuery():

    def __init__(self):
        self.MLSystemQueryController = MLSystemQueryController()

    def handle(self, job):
        logger.debug("MLSystemQuery流水线，正在运作")
        if 2 == job.system_type:
            self.MLSystemQueryController.errorSummary(job)






