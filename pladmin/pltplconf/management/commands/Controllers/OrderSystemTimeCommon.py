# -*- coding: utf8 -*-

import logging
import json
from pltplconf.management.commands.Collectors.OrderSystemCommonAnalysis import OrderSystemCommonAnalysis
from pltplconf.management.commands.Parsers.SendTimeFormate import SendTimeFormate
from pltplconf.management.commands.Messagers.WxTeamTime import WxTeamTime

logger = logging.getLogger(__name__)

class OrderSystemTimeCommon():

    def executeTime(self, job):
        logger.debug("OrderSystemTimeCommon控制器开始执行")
        queryLog = OrderSystemCommonAnalysis().findLogs(job.es_query, job.es_query_num)
        params = SendTimeFormate().parse(queryLog)
        params['job_name'] = job.job_name
        if params['total'] > 0:
            WxTeamTime().send(job, params)
        exit(0)


