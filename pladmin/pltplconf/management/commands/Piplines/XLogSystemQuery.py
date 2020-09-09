# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.XLogSystemQuery import XLogSystemQuery as XLogSystemQueryController
import logging

logger = logging.getLogger(__name__)

class XLogSystemQuery():

    def __init__(self):
        self.XLogSystemQueryController = XLogSystemQueryController()

    def handle(self, job):
        if 1 == job.system_type:
            logger.debug("XLogSystemQueryController流水线，正在处理，job=" + str(job))
            self.XLogSystemQueryController.query(job)






