# -*- coding: utf8 -*-

from elasticsearch import Elasticsearch
from django.forms.models import model_to_dict
import json

class ElasticsearchLongQuery:
    """应对需要大量数据导出处理"""

    _lastScrollId = ""
    _lastQueryResult = {}

    def __init__(self, request, cacheTime, startTime, endTime):
        self._esObject = getEsObject(request)
        self._request = request
        self._cacheTime = cacheTime
        self._startTime = startTime
        self._endTime = endTime

    def __iter__(self):
        return self

    def __next__(self):
        if "" == self._lastScrollId:
            self._lastQueryResult = self.firstQuery()
            self._lastScrollId = self._lastQueryResult["_scroll_id"]
            if 0 == len(self._lastQueryResult["hits"]["hits"]):
                raise StopIteration()
            return self._lastQueryResult
        self._lastQueryResult = self.nextQuery()
        #self._lastScrollId = self._lastQueryResult["_scroll_id"]
        if 0 == len(self._lastQueryResult["hits"]["hits"]):
            raise StopIteration()
        return self._lastQueryResult

    def firstQuery(self):
        datas = json.loads(self._request.body.decode())
        """执行首次 ES 查询"""
        return self._esObject.search(index=datas["params"]["query_type"], q=self.queryString(), ignore_unavailable=True, analyze_wildcard=True, size=1000, terminate_after=1000000, track_scores=False, scroll=self._cacheTime)

    def nextQuery(self):
        """执行非首次 ES 查询"""
        return self._esObject.scroll(scroll_id = self._lastScrollId, scroll = self._cacheTime)

    def queryString(self):
        datas = json.loads(self._request.body.decode())
        """获取查询的语句"""
        queryTime = "[" + getTimeformate(self._startTime) + " TO " + getTimeformate(self._endTime) + "]"
        if "" == datas["params"]["query_string"] or datas["params"]["query_string"] is None:
            return "@timestamp:" + queryTime + " OR timestamp:" + queryTime
        else:
            return datas["params"]["query_string"] + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"

# 模拟request的属性
class FakeRequest():
    """模拟Request对象"""
    def __init__(self, taskSetting):
        self.body = json.dumps({"params": model_to_dict(taskSetting)}).encode()

class FakeRequestFromDist():
    """模拟Request对象"""
    def __init__(self, taskSettingDist):
        self.body = json.dumps({"params": taskSettingDist}).encode()

def getTimeformate(dateTime):
    year = '%(value)04d'%{'value':dateTime.year}
    month = '%(value)02d'%{'value':dateTime.month}
    day = '%(value)02d'%{'value':dateTime.day}
    hour = '%(value)02d'%{'value':dateTime.hour}
    minute = '%(value)02d'%{'value':dateTime.minute}
    second = '%(value)02d'%{'value':dateTime.second}
    return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "+0800"

def getEsObject(request):
    """根据配置信息，返回一个ES对象"""
    datas = json.loads(request.body.decode())
    port = 80
    ssl = False
    if "https" == datas["params"]["es_sechma"]:
        port = 443
        ssl = True
    if "" != datas["params"]["es_port"]:
        port = int(datas["params"]["es_port"])
    ip = datas["params"]["es_ip"]
    if "" == datas["params"]["es_ip"] or datas["params"]["es_ip"] is None:
        ip = datas["params"]["es_host"]
    compress = False
    if 1 == datas["params"]["compress"]:
        compress = True
    auth = ""
    authUser = datas["params"]["auth_user"]
    if datas["params"]["auth_user"] is None:
        authUser = ""
    authPwd = datas["params"]["auth_pwd"]
    if datas["params"]["auth_pwd"] is None:
        authPwd = ""
    if "" != authPwd or "" != authPwd:
        auth = authUser + ":" + authPwd
    kbnVersion = ""
    if "kbn_version" in datas["params"]:
        kbnVersion = datas["params"]["kbn_version"]
    if kbnVersion is None:
        kbnVersion = ""

    urlPrefix = ""
    if "url_prefix" in datas["params"]:
        urlPrefix = datas["params"]["url_prefix"]
    if urlPrefix is None or "" == urlPrefix:
        h = {"host": ip, "port": port}
    else:
        h = {"host": ip, "port": port, "url_prefix": urlPrefix}
    return Elasticsearch(
        [h],
        headers={"kbn-version":kbnVersion,"Host":datas["params"]["es_host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+datas["params"]["es_host"]+"/app/kibana"},
        timeout=120,
        http_compress=compress,
        use_ssl=ssl,
        verify_certs=False,
        http_auth=auth
    )