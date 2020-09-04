# -*- coding: utf8 -*-

"""示例用
在Linux系统中命令行方式使用代理服务，方式是设置环境变量：
http_poxy="http://user:password@www.example.cn:1000"
https_poxy="http://user:password@www.example.cn:1000"
"""
from elasticsearch import Elasticsearch
import json
import time
from string import Template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OrderSystemCommonAnalysis():

    def findLogs(self, queryCommand, querySize = 1):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        logger.debug("es查询采集部分，收到命令：" + queryCommand + ",采集数量：" + str(querySize))
        es = Elasticsearch(
            [{"host": settings.ES_ADDRESS["ip"], "port": 80, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"4.5.4","Host":settings.ES_ADDRESS["host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            timeout=10,
            http_compress=False
        )
        # 模板里面的${queryCommand}必须经过JSON处理，转义
        query_data='''
{"index":["project_app-${today}"],"ignore_unavailable":true}
{"size":${querySize},"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"query":${queryCommand},"analyze_wildcard":true}},"filter":{"bool":{"must":[]}}}},"fields":["message"],"fielddata_fields":["@timestamp"]}
'''
        tpl = Template(query_data)
        return json.dumps(es.msearch(tpl.substitute(
            today = time.strftime("%Y.%m.%d"),
            querySize = querySize,
            queryCommand = json.dumps(queryCommand)
        )))

