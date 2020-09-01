# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.OrderCreateAnalysis import OrderCreateAnalysis
from pltplconf.management.commands.Parsers.DefaultLogFormate import DefaultLogFormate
from pltplconf.management.commands.Messagers.WxTeam import WxTeam
import logging

logger = logging.getLogger(__name__)

class OrderCreate():

    def orderCreateSuccessSummary(self):
        logger.debug("开始统计订单创建信息")
        queryLog = OrderCreateAnalysis().findLogs()
        params = DefaultLogFormate().parse(queryLog)
        if params['fail'] > 0:
            WxTeam().send(params)

