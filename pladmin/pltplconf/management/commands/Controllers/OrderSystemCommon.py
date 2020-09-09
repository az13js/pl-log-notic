# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.OrderSystemCommonAnalysis import OrderSystemCommonAnalysis
from pltplconf.management.commands.Parsers.DefaultLogFormate import DefaultLogFormate
from pltplconf.management.commands.Messagers.WxTeam import WxTeam
import logging

logger = logging.getLogger(__name__)

class OrderSystemCommon():

    def successSummary(self, job):
        logger.debug("控制器开始执行")
        queryLog = OrderSystemCommonAnalysis().findLogs(job.es_query, job.es_query_num)
        params = DefaultLogFormate().parse(queryLog)
        params['job_name'] = job.job_name
        if params['fail'] > 0:
            WxTeam().send(job, params)
        logger.debug("控制器执行完成")


