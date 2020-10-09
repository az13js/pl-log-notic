import json
import re
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
from pltplconf.models import Pljob, PlTaskSetting

@require_http_methods(["GET"])
def task_list(request):
    """返回任务列表"""
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
        task.save()
        result = response()
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="状态修改失败。")
    return result

@require_http_methods(["POST"])
@csrf_exempt
def task_test_es_link(request):
    """保存任务配置"""
    datas = json.loads(request.body.decode())
    try:
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
        es = Elasticsearch(
            [{"host": ip, "port": port, "url_prefix": "elasticsearch"}],
            headers={"Host":datas["params"]["es_host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+datas["params"]["es_host"]+"/app/kibana"},
            timeout=30,
            http_compress=compress,
            use_ssl=ssl,
            verify_certs=False,
            http_auth=auth
        )
        result = response(0, data={
            "esTestResult": es.info(),
            "debug": {
                "host": ip,
                "port": port,
                "headers": {"Host":datas["params"]["es_host"],"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0","Referer":"https://"+datas["params"]["es_host"]+"/app/kibana"},
                "http_compress": compress,
                "use_ssl": ssl,
                "http_auth": auth
            }
        })
    except ObjectDoesNotExist:
        result = response(-1, message="任务不存在，可能已经被删除。")
    except DatabaseError:
        result = response(-2, message="状态修改失败。")
    return result

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