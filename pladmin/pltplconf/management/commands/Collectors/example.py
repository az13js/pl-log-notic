# -*- coding: utf8 -*-

"""示例用
在Linux系统中命令行方式使用代理服务，方式是设置环境变量：
http_poxy="http://user:password@www.example.cn:1000"
https_poxy="http://user:password@www.example.cn:1000"
"""
from elasticsearch import Elasticsearch
import json

class example():
    def find(self):
        """find方法返回字符串，字符串内容是查询的消息文本"""
        # TODO 配置项： host，headers，放到数据库层面，json存储，转换，给应用用户灵活配置
        es = Elasticsearch(
            [{"host": "127.0.0.1", "port": 80, "url_prefix": "elasticsearch"}],
            headers={"kbn-version":"4.5.4","Host":"xxxxxxxx.cn","User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            timeout=10,
            http_compress=False
        )

        # TODO 配置项： query_data，放到数据库层面，json存储，转换，给应用用户灵活配置
        query_data='''
{"index":["project_app-2020.09.01"],"ignore_unavailable":true}
{"size":2,"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"query":"environment:\\"production\\" AND message:\\"goods_tree\\"","analyze_wildcard":true}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":1598941792528,"lte":1598942692528,"format":"epoch_millis"}}}]}}}},"fields":["message"],"fielddata_fields":["@timestamp"]}
'''
        results = es.msearch(query_data)
        return json.dumps(results)
