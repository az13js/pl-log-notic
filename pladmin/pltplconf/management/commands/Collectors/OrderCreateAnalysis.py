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
#import os

class OrderCreateAnalysis():

    def findLogs(self):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        # 本地临时测试
        #if os.path.isfile("/tmp/pl-log-notic-respond.txt"):
        #    fr = open("/tmp/pl-log-notic-respond.txt", "r")
        #    content = fr.read()
        #    fr.close()
        #    return content

        # TODO 配置项： host，headers，放到数据库层面，json存储，转换，给应用用户灵活配置
        es = Elasticsearch(
            [{"host": "127.0.0.1", "port": 80, "url_prefix": "elasticsearch"}],
            #[{"host": "127.0.0.1", "port": 80, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"4.5.4","Host":"example.com.cn","User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            #headers={"kbn-version":"4.5.4","Host":"xxxxxxxx.cn","User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            timeout=10,
            http_compress=False
        )

        # TODO 配置项： query_data，放到数据库层面，json存储，转换，给应用用户灵活配置
        query_data='''
{"index":["project_app-${today}"],"ignore_unavailable":true}
{"size":1000,"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"query":"environment:\\"production\\" AND message:\\"/order/create\\"","analyze_wildcard":true}},"filter":{"bool":{"must":[]}}}},"fields":["message"],"fielddata_fields":["@timestamp"]}
'''
        tpl = Template(query_data)
        return json.dumps(es.msearch(tpl.substitute(today=time.strftime("%Y.%m.%d"))))

