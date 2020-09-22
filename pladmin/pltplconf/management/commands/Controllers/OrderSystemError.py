# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.OrderSystemErrorAnalysis import OrderSystemErrorAnalysis
from pltplconf.management.commands.Parsers.ErrorFormate import ErrorFormate
from pltplconf.management.commands.Messagers.WxTeamErrorLog import WxTeamErrorLog
import logging

logger = logging.getLogger(__name__)

class OrderSystemError():

    def errorSummary(self, job):
        logger.debug("OrderSystemError 控制器开始执行，JOB=" + str(job))
        queryLog = OrderSystemErrorAnalysis().findErrorLogs(job)
        params = ErrorFormate().parse(queryLog)
        params['job_name'] = job.job_name
        if params['total'] > 0:
            WxTeamErrorLog().send(job, params)
        logger.debug("OrderSystemError 控制器执行完成")







