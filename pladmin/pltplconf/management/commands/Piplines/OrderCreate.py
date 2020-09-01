# -*- coding: utf8 -*-

from pltplconf.management.commands.Controllers.OrderCreate import OrderCreate as OrderCreateController
import logging

logger = logging.getLogger(__name__)

class OrderCreate():

    def __init__(self):
        self.orderCreateController = OrderCreateController()

    def handle(self, job):
        logger.debug("OrderCreate流水线，正在处理，job=" + str(job))
        self.orderCreateController.orderCreateSuccessSummary()






