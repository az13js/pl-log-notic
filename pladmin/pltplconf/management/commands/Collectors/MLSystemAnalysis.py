# -*- coding: utf8 -*-

from elasticsearch import Elasticsearch
import json
import datetime
from string import Template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MLSystemAnalysis():

    def findErrorLogs(self, queryCommand, querySize = 1):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        logger.debug("es查询采集部分，收到命令：" + queryCommand + ",采集数量：" + str(querySize))
        es = Elasticsearch(
            [{"host": settings.MLES_ADDRESS["ip"], "port": 443, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"7.5.2","Host":settings.MLES_ADDRESS["host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+settings.XES_ADDRESS["host"]+"/app/kibana"},
            timeout=30,
            http_compress=False,
            use_ssl=True,
            verify_certs=False,
            http_auth=settings.MLES_ADDRESS["http_auth"]
        )
        query_data='''
{"index":"err-prod-*","ignore_unavailable":true}
{"size":${querySize},"query":{"bool":{"filter":[{"match_phrase":{"project":{"query":"${project}"}}},{"range":{"timestamp":{"format":"strict_date_optional_time","gte":"${timestampMsStart}","lte":"${timestampMsEnd}"}}}]}}}
'''
        tpl = Template(query_data)
        return json.dumps(es.msearch(tpl.substitute(
            querySize = querySize,
            timestampMsStart = (datetime.datetime.utcnow() - datetime.timedelta(seconds = int(queryCommand))).isoformat() + 'Z',
            timestampMsEnd = datetime.datetime.utcnow().isoformat() + 'Z',
            project = settings.MLES_ADDRESS["project"]
        )))

