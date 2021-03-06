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
from pltplconf.management.commands.Collectors.ElasticsearchLongQuery import getEsObject, getTimeformate, FakeRequest
from pltplconf.models import Pljob, PlTaskSetting, PlExportJob
from pltplconf.management.commands.Parsers.TaskParser import TaskParser

######################## 支持异常检测然后报警推送 ########################

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
        task.url_prefix = datas["params"]["url_prefix"]
        task.es_port = datas["params"]["es_port"]
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
    searchResult = doQuery(getEsObject(request), datas["params"]["query_type"], datas["params"]["query_string"], datetime.now() - timedelta(days=1))
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

######################## 导出大量数据 ########################

@require_http_methods(["POST"])
@csrf_exempt
def task_export_test(request):
    """测试导出"""
    try:
        datas = json.loads(request.body.decode())
        taskSetting = PlTaskSetting.objects.get(id=datas["params"]["id"])
        es = getEsObject(FakeRequest(taskSetting))
        startTime = datetime.strptime(datas["params"]["setting"]["startDate"] + " " + datas["params"]["setting"]["startTime"], "%Y-%m-%d %H:%M:%S")
        endTime = datetime.strptime(datas["params"]["setting"]["endDate"] + " " + datas["params"]["setting"]["endTime"], "%Y-%m-%d %H:%M:%S")
        queryResult = doQuery(es, taskSetting.query_type, taskSetting.query_string, startTime, endTime)
        message = TaskParser().parse(taskSetting, queryResult.encode("utf-8").decode("unicode_escape"), datas["params"]["setting"]["template"])
        result = response(0, data={"result": message})
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="数据库查询异常")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_export_commit(request):
    """提交导出任务"""
    try:
        datas = json.loads(request.body.decode())
        taskSetting = PlTaskSetting.objects.get(id=datas["params"]["id"])
        try:
            exportJob = PlExportJob.objects.get(task_setting_id=taskSetting.id)
        except ObjectDoesNotExist:
            exportJob = PlExportJob(task_setting_id=taskSetting.id, run_time=timezone.now() - timedelta(weeks=100))
            exportJob.save() # 先保存一遍，保证数据库中一定存在，因为下面要使用update语句更新符合条件的这个任务，防止并发问题
        if 0 != exportJob.status:
            return response(-3, message="已经有导出任务提交，请先终止")

        # 执行更新，使用更新带条件操作是为了防止并发
        updateRows = PlExportJob.objects.filter(task_setting_id=taskSetting.id, status=0).update(
            status = 1,
            req_stop = 0,
            process = 0,
            worker_name = "",
            download_addr = "",
            task_setting_info = json.dumps(model_to_dict(taskSetting)),
            export_setting_info = json.dumps(datas["params"]["setting"])
        )
        if updateRows <= 0:
            return response(-4, message="更新失败")

        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="监控任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="数据库查询异常")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_export_cancel(request):
    """用户请求取消任务"""
    try:
        datas = json.loads(request.body.decode())
        updateRows = PlExportJob.objects.filter(task_setting_id=datas["params"]["id"],status=1).update(status=0,req_stop=0)
        if updateRows <= 0:
            updateRows = PlExportJob.objects.filter(task_setting_id=datas["params"]["id"],status=2).update(req_stop=1)
        if updateRows <= 0:
            return response(-3, message="导出任务不存在或任务不是已提交/运行中状态，无法接受取消")
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="导出任务不存在或任务不是已提交/运行中状态，无法接受取消")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_export_force_cancel(request):
    """用户请求取消任务"""
    try:
        datas = json.loads(request.body.decode())
        exportJob = PlExportJob.objects.get(task_setting_id=datas["params"]["id"])
        exportJob.status = 0
        exportJob.req_stop = 0
        exportJob.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="导出任务不存在")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["GET"])
def export_job_info(request):
    """查询导出任务信息"""
    try:
        if "id" in request.GET:
            exportJob = PlExportJob.objects.get(task_setting_id=int(request.GET["id"]))
            result = response(0, data={"exportJob": model_to_dict(exportJob)})
        else:
            exportJobs = []
            for exportJob in PlExportJob.objects.filter(task_setting_id__in=[i for i in map(lambda x:int(x), request.GET["ids"].split(','))]):
                exportJobs.append(model_to_dict(exportJob))
            result = response(0, data={"exportJobs": exportJobs})

    except ObjectDoesNotExist:
        result = response(-1, message="导出任务不存在。")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["GET"])
def export_commit_jobs(request):
    """查询已提交导出任务"""
    ids = []
    for job in PlExportJob.objects.filter(status=1, req_stop=0):
        ids.append(job.task_setting_id)
    return response(0, data={"taskSettingIds": ids})

@require_http_methods(["POST"])
@csrf_exempt
def worker_recv_export_job(request):
    """Worker进程（集群节点）请求接受给定ID（taskSettingId）的导出任务"""
    try:
        datas = json.loads(request.body.decode())
        taskSettingId = int(datas["params"]["taskSettingId"])
        # Worker进程可以有多个，为了防止并发请求导致job更新不及时被两个Worker消费，这里需要这样处理
        updateRows = PlExportJob.objects.filter(task_setting_id=taskSettingId,status=1,req_stop=0).update(
            status = 2, # 更改为运行中
            worker_name = datas["params"]["workerName"],
            run_time = timezone.now()
        )
        if updateRows <= 0:
            return response(-3, message="符合领取条件的数据库记录不存在，或取消，或已被领取")

        # 返回导出任务的信息，Worker需要根据这些信息运作
        result = response(0, data={
            "exportJob": model_to_dict(PlExportJob.objects.get(task_setting_id=taskSettingId))
        })
    except ObjectDoesNotExist:
        result = response(-1, message="数据库记录不存在")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def worker_process(request):
    """Worker进程向服务器同步处理进度消息"""
    try:
        datas = json.loads(request.body.decode())
        exportJob = PlExportJob.objects.get(task_setting_id=datas["params"]["taskSettingId"],status=2)
        if 1 == exportJob.req_stop:
            return response(-101, message="用户请求停止任务，无需再同步进度")
        exportJob.process = datas["params"]["process"]
        exportJob.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="导出任务不存在或任务不是运行中状态，无法接受同步")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def worker_finish(request):
    """Worker进程向服务器同步处理结果"""
    try:
        datas = json.loads(request.body.decode())
        exportJob = PlExportJob.objects.get(task_setting_id=datas["params"]["taskSettingId"],status=2)
        exportJob.status = 0
        exportJob.req_stop = 0
        exportJob.process = datas["params"]["process"]
        exportJob.download_addr = datas["params"]["downloadAddress"]
        exportJob.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="导出任务不存在或任务不是运行中状态，无法接受同步")
    except DatabaseError:
        result = response(-2, message="查询数据异常。")
    return result

######################## TODO 下面需要支持流量检测然后报警推送 ########################

######################## 共用函数 ########################

def doQuery(esObject, queryType, queryString, gte, endTime = None):
    """
        执行 ES 查询
    参数：
        esObject: ES对象
        queryType: 查询的index
        queryString: 查询的语句
        gte: 一个datetime对象，查询的开始时间
        endTime: 默认是 None，可以传一个结束时间，datetime对象
    返回值：字符串
    """
    realQueryString = queryString
    if endTime is None:
        queryTime = "[" + getTimeformate(gte) + " TO " + getTimeformate(datetime.now()) + "]"
    else:
        queryTime = "[" + getTimeformate(gte) + " TO " + getTimeformate(endTime) + "]"
    if "" == realQueryString or realQueryString is None:
        realQueryString = "@timestamp:" + queryTime + " OR timestamp:" + queryTime
    else:
        realQueryString = realQueryString + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"
    return json.dumps(esObject.search(index=queryType, q=realQueryString, ignore_unavailable=True, analyze_wildcard=True, size=100, track_scores=False, terminate_after=100))

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
