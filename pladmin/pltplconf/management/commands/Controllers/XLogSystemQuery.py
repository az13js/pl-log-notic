# -*- coding: utf8 -*-

import logging
from pltplconf.management.commands.Collectors.XLogSystemQuery import XLogSystemQuery as XLogSystemQueryCollector
from pltplconf.management.commands.Parsers.XLogFormate import XLogFormate
from pltplconf.management.commands.Messagers.WxTeamXLog import WxTeamXLog

logger = logging.getLogger(__name__)

class XLogSystemQuery():

    def query(self, job):
        logger.debug("XLogSystemQuery控制器开始执行")
        queryLog = XLogSystemQueryCollector().findLogs(job.es_query, job.es_query_num)
        params = XLogFormate().parse(queryLog)
        if params['total'] > 0:
            params["job_name"] = job.job_name
            WxTeamXLog().send(job, params)



