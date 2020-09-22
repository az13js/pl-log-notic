# -*- coding: utf8 -*-

from elasticsearch import Elasticsearch
import json
import time
from string import Template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OrderSystemErrorAnalysis():

    def findErrorLogs(self, job):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        logger.debug("es查询采集部分，收到命令：" + job.es_query + ",采集数量：" + str(job.es_query_num))
        es = Elasticsearch(
            [{"host": settings.ES_ADDRESS["ip"], "port": 80, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"4.5.4","Host":settings.ES_ADDRESS["host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            timeout=10,
            http_compress=False
        )
        # 模板里面的${queryCommand}必须经过JSON处理，转义
        query_data='''
{"index":["project_err-*"],"ignore_unavailable":true}
{"size":${querySize},"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":${queryCommand}}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":${timestampMsStart},"lte":${timestampMsEnd},"format":"epoch_millis"}}}],"must_not":[]}}}},"fields":["*","_source"],"script_fields":{},"fielddata_fields":["@timestamp"]}
'''
        tpl = Template(query_data)
        return json.dumps(es.msearch(tpl.substitute(
            querySize = job.es_query_num,
            timestampMsStart = round((time.time() - float(job.delay_sec) - 2 * 60) * 1000),
            timestampMsEnd = round(time.time() * 1000),
            queryCommand = json.dumps(job.es_query)
        )))

