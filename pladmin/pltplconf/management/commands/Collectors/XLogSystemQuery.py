# -*- coding: utf8 -*-

from elasticsearch import Elasticsearch
import json
import time
from string import Template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class XLogSystemQuery():

    def findLogs(self, queryCommand, querySize = 1):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        logger.debug("es查询采集部分，收到命令：" + queryCommand + ",采集数量：" + str(querySize))
        es = Elasticsearch(
            [{"host": settings.XES_ADDRESS["ip"], "port": 443, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"6.3.2","Host":settings.XES_ADDRESS["host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+settings.XES_ADDRESS["host"]+"/app/kibana"},
            timeout=30,
            http_compress=False,
            use_ssl=True,
            verify_certs=False,
            http_auth=settings.XES_ADDRESS["http_auth"]
        )
        # 模板里面的${queryCommand}必须经过JSON处理，转义
        query_data='''
{"index":"err-prod*","ignore_unavailable":true,"timeout":30000}
{"size":${querySize},"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"bool":{"must":[{"match_phrase":{"project":{"query":"ms-order-crm"}}},{"match_phrase":{"env":{"query":"prod"}}},{"range":{"timestamp":{"gte":${timestampMsStart},"lte":${timestampMsEnd},"format":"epoch_millis"}}}]}}}
'''
        tpl = Template(query_data)
        return json.dumps(es.msearch(tpl.substitute(
            querySize = querySize,
            timestampMsStart = round((time.time() - float(queryCommand)) * 1000),
            timestampMsEnd = round(time.time() * 1000)
        )))

