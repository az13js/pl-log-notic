import json
import re
import time
import requests
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction, DatabaseError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.forms.models import model_to_dict
from elasticsearch import Elasticsearch
from string import Template
from pltplconf.models import Pljob, PlTaskSetting

@require_http_methods(["GET"])
def task_list(request):
    """返回任务列表"""
    taskName = request.GET.get('taskName')
    if "" != taskName and taskName is not None:
        tasks = PlTaskSetting.objects.filter(task_name__icontains=taskName).order_by('-id').all()
    else:
        tasks = PlTaskSetting.objects.order_by('-id').all()
    paginator = Paginator(tasks, 5)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = []
    results = []
    for task in list:
        results.append({"id": task.id, "name": task.task_name, "status": task.status})
    return response(data={
        "list": results
    })

@require_http_methods(["POST"])
@csrf_exempt
def task_add(request):
    """新建任务，不包含详细的配置，只有名称"""
    datas = json.loads(request.body.decode())
    params = datas["params"]

    # 任务名称不能为空
    if re.compile(r"^\s*$").match(params["taskName"]) is not None:
        return response(-1, message="任务名不能为空。")

    # 如果数据库中已经有名称相同的任务，那么不能重复创建
    if PlTaskSetting.objects.filter(task_name=params["taskName"]).count() > 0:
        return response(-2, message="任务名已存在，无法重复创建。")

    taskSetting = PlTaskSetting(task_name=params["taskName"])
    job = Pljob(
        last_exec_time = timezone.now(),
        next_exec_time = timezone.now(),
        delay_sec = 1,
        job_name = taskSetting.task_name,
        task_setting = taskSetting,
        system_type = 5 # 5 专门表示关联 PlTaskSetting 的
    )

    success = True
    try:
        with transaction.atomic():
            taskSetting.save()
            job.save()
    except DatabaseError:
        success = False

    if success:
        return response(0, data={"id": taskSetting.id})
    else:
        return response(1)

@require_http_methods(["POST"])
@csrf_exempt
def task_delete(request):
    """删除指定的任务"""
    datas = json.loads(request.body.decode())
    try:
        task = PlTaskSetting.objects.get(id=datas["params"]["id"])
        task.delete()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已在其它网页端被删除。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_set_status(request):
    """设置任务的开启、关闭状态"""
    datas = json.loads(request.body.decode())
    try:
        task = PlTaskSetting.objects.get(id=datas["params"]["id"])
        task.status = datas["params"]["status"]
        task.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="状态修改失败。")
    return result

@require_http_methods(["GET"])
@csrf_exempt
def task_info(request):
    """任务信息"""
    try:
        task = model_to_dict(PlTaskSetting.objects.get(id=request.GET["id"]))
        result = response(0, data={"task": task})
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_save_info(request):
    """保存任务配置"""
    datas = json.loads(request.body.decode())
    try:
        task = PlTaskSetting.objects.get(id=datas["params"]["id"])
        task.es_host = datas["params"]["es_host"]
        task.es_ip = datas["params"]["es_ip"]
        task.es_sechma = datas["params"]["es_sechma"]
        task.compress = datas["params"]["compress"]
        task.auth_user = datas["params"]["auth_user"]
        task.auth_pwd = datas["params"]["auth_pwd"]
        task.query_string = datas["params"]["query_string"]
        task.query_type = datas["params"]["query_type"]
        task.wx_bot_addr = datas["params"]["wx_bot_addr"]
        task.template = datas["params"]["template"]
        task.placeholders = datas["params"]["placeholders"]
        task.delay_sec = datas["params"]["delay_sec"]
        task.push_min = datas["params"]["push_min"]
        task.max_per_hour = datas["params"]["max_per_hour"]
        task.kbn_version = datas["params"]["kbn_version"]
        job = Pljob.objects.get(task_setting=task)
        job.delay_sec = task.delay_sec
        task.save()
        job.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="状态修改失败。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_test_es_link(request):
    """测试ES连接配置"""
    return response(0, data={"esTestResult": getEsObject(request).info()})

@require_http_methods(["POST"])
@csrf_exempt
def task_test_wxbot_address(request):
    """测试企业微信地址"""
    datas = json.loads(request.body.decode())
    address = datas["params"]["wx_bot_addr"]
    data = {
        "msgtype": "text",
        "text": {
            "content": "【企业微信机器人测试消息】大家好。"
        }
    }
    return response(0, data={
        "wxTestResult": requests.post(url = address, headers = {"Content-Type": "text/plain"}, json = data).content.decode()
    })

@require_http_methods(["POST"])
@csrf_exempt
def task_test_es_query(request):
    """保存任务配置"""
    datas = json.loads(request.body.decode())
    searchResult = doQuery(getEsObject(request), datas["params"]["query_type"], datas["params"]["query_string"], datetime.now(timezone.utc) - timedelta(days=1))
    return response(0, data={"esQueryResult": searchResult.encode("utf-8").decode("unicode_escape")})
    #return response(0, data={"esQueryResult": searchResult})

@require_http_methods(["POST"])
@csrf_exempt
def task_test_send_template(request):
    """测试发送模板"""
    datas = json.loads(request.body.decode())
    address = datas["params"]["wx_bot_addr"]
    data = {
        "msgtype": "text",
        "text": {
            "content": datas["params"]["template"]
        }
    }
    return response(0, data={
        "sendResult": requests.post(url = address, headers = {"Content-Type": "text/plain"}, json = data).content.decode()
    })

def getEsObject(request):
    """根据配置信息，返回一个ES对象"""
    datas = json.loads(request.body.decode())
    port = 80
    ssl = False
    if "https" == datas["params"]["es_sechma"]:
        port = 443
        ssl = True
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
    return Elasticsearch(
        [{"host": ip, "port": port, "url_prefix": "elasticsearch"}],
        headers={"kbn-version":kbnVersion,"Host":datas["params"]["es_host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+datas["params"]["es_host"]+"/app/kibana"},
        timeout=30,
        http_compress=compress,
        use_ssl=ssl,
        verify_certs=False,
        http_auth=auth
    )

def doQuery(esObject, queryType, queryString, gte):
    """执行 ES 查询"""
    realQueryString = queryString
    queryTime = "[" + getTimeformate(gte) + " TO " + getTimeformate(datetime.now(timezone.utc)) + "]"
    if "" == realQueryString or realQueryString is None:
        realQueryString = "@timestamp:" + queryTime + " OR timestamp:" + queryTime
    else:
        realQueryString = realQueryString + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"
    return json.dumps(esObject.search(index=queryType, q=realQueryString, ignore_unavailable=True, analyze_wildcard=True, size=100, track_scores=False, terminate_after=100))

def getTimeformate(dateTime):
    #dateTime = datetime.now(timezone.utc)
    year = '%(value)04d'%{'value':dateTime.year}
    month = '%(value)02d'%{'value':dateTime.month}
    day = '%(value)02d'%{'value':dateTime.day}
    hour = '%(value)02d'%{'value':dateTime.hour}
    minute = '%(value)02d'%{'value':dateTime.minute}
    second = '%(value)02d'%{'value':dateTime.second}
    return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "Z"

def response(code=0, data={}, message=""):
    """统一返回格式"""
    codes = { # 公共的返回消息，code >= 0，如果业务需要返回定制消息的，code取负数
        0: "success",
        1: "数据库写入失败"
    }
    if code in codes:
        return JsonResponse({"code": code, "message": codes[code], "data": data})
    else:
        return JsonResponse({"code": code, "message": message, "data": data})

def fixQuery(job, startTime, endTime):
    """临时函数，导出 ES 测试"""
    i = 0
    for r in ElasticsearchFromQuery(FakeRequestX(job.task_setting), startTime, endTime):
        fw = open("p" + str(i) + ".json", "w")
        fw.write(json.dumps(r))
        fw.close()
        i = i + 1
    exit(0)

# 模拟request的属性
class FakeRequestX():
    """临时类，导出 ES 测试"""
    def __init__(self, taskSetting):
        self.body = json.dumps({"params": model_to_dict(taskSetting)}).encode()

class ElasticsearchLongQuery:
    """临时测试，应对需要大量数据导出处理"""

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
                return StopIteration()
            return self._lastQueryResult
        self._lastQueryResult = self.nextQuery()
        self._lastScrollId = self._lastQueryResult["_scroll_id"]
        if 0 == len(self._lastQueryResult["hits"]["hits"]):
            return StopIteration()
        return self._lastQueryResult

    def firstQuery(self):
        datas = json.loads(self._request.body.decode())
        """执行首次 ES 查询"""
        return self._esObject.search(index=datas["params"]["query_type"], q=self.queryString(), ignore_unavailable=True, analyze_wildcard=True, size=10, terminate_after=10000, track_scores=False, scroll=self._cacheTime)

    def nextQuery(self):
        """执行非首次 ES 查询"""
        return self._esObject.search(json.dumps({"scroll_id": self._lastScrollId}), ignore_unavailable=True, analyze_wildcard=True, size=10, terminate_after=10000, track_scores=False, scroll=self._cacheTime)

    def queryString(self):
        datas = json.loads(self._request.body.decode())
        """获取查询的语句"""
        queryTime = "[" + getTimeformate(self._startTime) + " TO " + getTimeformate(self._endTime) + "]"
        if "" == datas["params"]["query_string"] or datas["params"]["query_string"] is None:
            return "@timestamp:" + queryTime + " OR timestamp:" + queryTime
        else:
            return datas["params"]["query_string"] + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"

class ElasticsearchFromQuery:
    """临时测试，应对需要大量数据导出处理"""

    _lastFrom = 0
    _size = 10
    _lastQueryResult = {}

    def __init__(self, request, startTime, endTime):
        self._esObject = getEsObject(request)
        self._request = request
        self._startTime = startTime
        self._endTime = endTime

    def __iter__(self):
        return self

    def __next__(self):
        self._lastQueryResult = self.doQuery()
        if 0 == len(self._lastQueryResult["hits"]["hits"]):
            return StopIteration()
        self._lastFrom = self._lastFrom + self._size
        return self._lastQueryResult

    def doQuery(self):
        datas = json.loads(self._request.body.decode())
        """执行首次 ES 查询"""
        return self._esObject.search(index=datas["params"]["query_type"], q=self.queryString(), ignore_unavailable=True, analyze_wildcard=True, size=self._size, from_ = self._lastFrom, terminate_after=10000, track_scores=False)

    def queryString(self):
        datas = json.loads(self._request.body.decode())
        """获取查询的语句"""
        queryTime = "[" + getTimeformate(self._startTime) + " TO " + getTimeformate(self._endTime) + "]"
        if "" == datas["params"]["query_string"] or datas["params"]["query_string"] is None:
            return "@timestamp:" + queryTime + " OR timestamp:" + queryTime
        else:
            return datas["params"]["query_string"] + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"
