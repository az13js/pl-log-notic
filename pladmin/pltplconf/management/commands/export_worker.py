# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from pltplconf.models import Pljob, PlTaskSetting
from django.utils import timezone
import datetime
from django.forms.models import model_to_dict
from pltplconf import api
import json
import os
from django.core.exceptions import ObjectDoesNotExist
from pltplconf.management.commands.Parsers.TaskParser import TaskParser

class Command(BaseCommand):
    help = "后台导出 ES 数据工作进程"

    def handle(self, *args, **options):
        """
            命令行导出大量日志，从ES作为数据来源
        使用的时候需要设置一些环境变量：

        JOB_NAME  任务的名称，这个在web界面监控列表可以看到，这个JOB会作为查询方式和通配符配置
        START     开始时间，例如：2020-10-20T00:00:00+08:00，字符串
        END       结束时间，例如：2020-10-20T01:00:00+08:00，字符串
        FLODER    文件夹，导出的数据存在里面
        CACHETIME 游标缓存时间 1m 表示1分钟

            示例：
        JOB_NAME="测试任务" START="2020-10-21T00:00:00+08:00" END="2020-10-21T10:00:00+08:00" FLODER="/tmp/exports" CACHETIME="5m" python3 manage.py export_worker
        """
        self.stdout.write(self.style.SUCCESS("命令行进程启动"))
        if not "JOB_NAME" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量：JOB_NAME"))
            return
        if not "START" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量：START"))
            return
        if not "END" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量：END"))
            return
        if not "FLODER" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量：FLODER"))
            return
        if not "CACHETIME" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量：CACHETIME"))
            return
        try:
            task = PlTaskSetting.objects.get(task_name=os.environ["JOB_NAME"])
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR("任务不存在"))
            return
        job = Pljob.objects.get(task_setting = task)
        startTimeObject = datetime.datetime.fromisoformat(os.environ["START"])
        endTimeObject = datetime.datetime.fromisoformat(os.environ["END"])
        if not os.path.isdir(os.environ["FLODER"]):
            os.makedirs(os.environ["FLODER"])
        if not os.path.isdir(os.environ["FLODER"]):
            self.stdout.write(self.style.ERROR("目录不存在且创建目录失败"))
            return
        self.fetchDataToFloder(job, startTimeObject, endTimeObject, os.environ["CACHETIME"], os.environ["FLODER"])
        self.stdout.write(self.style.SUCCESS("导出完成"))

    def fetchDataToFloder(self, job, startTime, endTime, cacheTime, floder):
        """
            大型数据从 ES 导出处理
        参数：
            job: 后台job对象
            startTime: 查询开始时间，包含，是个日期对象
            endTime: 查询结束时间，包含，是个日期对象
            cacheTime: 缓存时间，是个字符串，比如 1m 是1分钟
            floder: 一个文件夹。如果文件夹不存在会尝试建立文件夹
        返回值:
            不返回什么有用的返回值
        """
        i = 0
        try:
            for distResult in ElasticsearchLongQuery(FakeRequest(job.task_setting), cacheTime, startTime, endTime):
                message = TaskParser().parse(job.task_setting, json.dumps(distResult).encode("utf-8").decode("unicode_escape"))
                fw = open(floder + os.sep + str(i) + ".txt", "w")
                fw.write(message)
                fw.close()
                i = i + 1
        except StopIteration:
            return

# 模拟request的属性
class FakeRequest():
    """模拟Request对象"""
    def __init__(self, taskSetting):
        self.body = json.dumps({"params": model_to_dict(taskSetting)}).encode()

class ElasticsearchLongQuery:
    """应对需要大量数据导出处理"""

    _lastScrollId = ""
    _lastQueryResult = {}

    def __init__(self, request, cacheTime, startTime, endTime):
        self._esObject = api.getEsObject(request)
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
        queryTime = "[" + api.getTimeformate(self._startTime) + " TO " + api.getTimeformate(self._endTime) + "]"
        if "" == datas["params"]["query_string"] or datas["params"]["query_string"] is None:
            return "@timestamp:" + queryTime + " OR timestamp:" + queryTime
        else:
            return datas["params"]["query_string"] + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"
