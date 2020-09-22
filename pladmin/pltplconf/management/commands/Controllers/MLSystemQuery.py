# -*- coding: utf8 -*-

from pltplconf.management.commands.Collectors.MLSystemAnalysis import MLSystemAnalysis
from pltplconf.management.commands.Parsers.MLFormate import MLFormate
from pltplconf.management.commands.Messagers.WxTeamXLog import WxTeamXLog
import logging

logger = logging.getLogger(__name__)

class MLSystemQuery():

    def errorSummary(self, job):
        logger.debug("MLSystemQuery控制器开始执行，JOB=" + str(job))
        queryLog = MLSystemAnalysis().findErrorLogs(job.es_query, job.es_query_num)
        params = MLFormate().parse(queryLog)
        params['job_name'] = job.job_name
        if params['total'] > 0:
            WxTeamXLog().send(job, params)
        logger.debug("MLSystemQuery控制器执行完成")






