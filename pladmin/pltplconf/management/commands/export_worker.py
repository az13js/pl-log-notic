# -*- coding: utf8 -*-

import os
import time
import uuid
import json
import shutil
import random
import logging
import requests
import subprocess
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from pltplconf.management.commands.Parsers.TaskParser import TaskParser
from pltplconf.management.commands.Collectors.ElasticsearchLongQuery import getEsObject, FakeRequestFromDist, getTimeformate, ElasticsearchLongQuery

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "后台导出 ES 数据工作进程"

    def handle(self, *args, **options):
        """
            Worker节点进程
        详情请参考README.md中关于集群节点的介绍。
        """

        self.stdout.write(self.style.SUCCESS("Worker进程启动"))

        # 检查启动参数的完整性

        if not "WORKER_NAME" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量： WORKER_NAME"))
            return
        else:
            workerName = os.environ["WORKER_NAME"]

        if not "HOST" in os.environ:
            self.stdout.write(self.style.ERROR("缺少环境变量： HOST"))
            return
        else:
            host = os.environ["HOST"]

        if not "IP" in os.environ:
            ip = host
        else:
            ip = os.environ["IP"]

        port = "80"
        if "PORT" in os.environ:
            port = os.environ["PORT"]

        cacheTime = "1m"
        if "CACHETIME" in os.environ:
            cacheTime = os.environ["CACHETIME"]

        authUser = ""
        if "USER" in os.environ:
            authUser = os.environ["USER"]

        password = ""
        if "PASSWORD" in os.environ:
            password = os.environ["PASSWORD"]

        self.stdout.write(self.style.SUCCESS(
            "启动参数：\n"
            + "WORKER_NAME=" + workerName + "\n"
            + "HOST=" + host + "\n"
            + "IP=" + ip + "\n"
            + "PORT=" + port + "\n"
            + "CACHETIME=" + cacheTime + "\n"
            + "USER=" + authUser + "\n"
            + "PASSWORD=" + password
        ))
        self._workerName = workerName
        self._host = host
        self._ip = ip
        self._port = port
        self._cacheTime = cacheTime
        self._authUser = authUser
        self._password = password

        # 循环查询可执行任务列表，并执行
        while True:
            try:
                ids = self.getListIds()
                if len(ids) > 0:
                    id = random.choice(ids)
                    response = self.recv(id)
                    if 0 == response["code"]:
                        self._serverResponse = response
                        if False == self.prepareFloder():
                            self.sendCancelSuccess(id)
                            break
                        if self.doExportLoop(id):
                            """正常导出完成"""
                            downloadUrl = self.callExecuteCommand(self._floder)
                            self.sendExportSuccess(id, downloadUrl)
                        else:
                            self.sendCancelSuccess(id)
                        self.cleanFloder()
                time.sleep(random.random() * 6)
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("命令停止"))
                exit(0)

    def getListIds(self):
        """查询等待被导出的任务"""
        baseAddress = "http://" + self._ip + ":" + self._port
        result = requests.get(baseAddress + "/pl/communicate/export-commit-jobs", headers={"host": self._host}, auth=(self._authUser,self._password))
        try:
            data = result.json()
        except ValueError:
            data = {"code":0,"data": {"taskSettingIds": []}}
        if 0 == data["code"]:
            return data["data"]["taskSettingIds"]
        return []

    def recv(self, id):
        """接收给定ID的导出任务"""
        baseAddress = "http://" + self._ip + ":" + self._port
        result = requests.post(
            url=baseAddress + "/pl/communicate/worker-recv-export-job",
            json={"params":{"taskSettingId":int(id),"workerName":self._workerName}},
            headers={"host": self._host},
            auth=(self._authUser,self._password)
        )
        try:
            data = result.json()
        except ValueError:
            data = {"code":-1000}
        return data

    def doExportLoop(self, id):
        """根据服务器返回的接受成功的相应结果导出数据"""
        exportSettingDist = json.loads(self._serverResponse["data"]["exportJob"]["export_setting_info"])
        taskSettingDist = json.loads(self._serverResponse["data"]["exportJob"]["task_setting_info"])
        # 暂时就按照东8区来算，反正老外不可能用我这个系统的
        startTime = datetime.fromisoformat(exportSettingDist["startDate"] + "T" + exportSettingDist["startTime"] + "+08:00")
        endTime = datetime.fromisoformat(exportSettingDist["endDate"] + "T" + exportSettingDist["endTime"] + "+08:00")
        fakeRequest = FakeRequestFromDist(taskSettingDist)
        #es = getEsObject(fakeRequest)
        # 计算要导出的数据的总数，用来计算导出的进度（不可用，暂时不这样计算了）
        #total = es.count(
        #    index=taskSettingDist["query_type"],
        #    ignore_unavailable=True, analyze_wildcard=True,
        #    terminate_after=1000000,
        #    q=self.queryString(taskSettingDist["query_string"],startTime,endTime)
        #)
        total = None
        exportNum = 0
        i = 0
        try:
            for distResult in ElasticsearchLongQuery(fakeRequest, self._cacheTime, startTime, endTime):
                if "hits" in distResult and "total" in distResult["hits"] and total is None:
                    total = int(distResult["hits"]["total"])
                message = TaskParser().parseDist(taskSettingDist, json.dumps(distResult).encode("utf-8").decode("unicode_escape"), exportSettingDist["template"])
                with open(self._floder + os.sep + str(i) + ".txt", "w") as fw:
                    fw.write(message)
                i = i + 1
                if "hits" in distResult and "hits" in distResult["hits"] and total is not None:
                    exportNum = exportNum + len(distResult["hits"]["hits"])
                    process = exportNum / total
                else:
                    process = i / 10000
                if process > 0.99:
                    process = 0.99
                if False == self.sendProcess(id, process):
                    return False
        except StopIteration:
            return True
        return True

    def callExecuteCommand(self, floder):
        """调用第三方命令进行文件处理"""
        logger.debug("执行命令： " + settings.EXPORT_FLODER_PROCESS_COMMAND + " \"" + floder + "\"")
        result = subprocess.run(settings.EXPORT_FLODER_PROCESS_COMMAND + " \"" + floder + "\"", shell=True, universal_newlines=True, stdout=subprocess.PIPE)
        if result.returncode != 0:
            return ""
        return str(result.stdout).strip()

    def sendProcess(self, id, process):
        baseAddress = "http://" + self._ip + ":" + self._port
        result = requests.post(
            url=baseAddress + "/pl/communicate/worker-process",
            json={"params":{"taskSettingId":int(id),"process":process}},
            headers={"host": self._host},
            auth=(self._authUser,self._password)
        )
        try:
            data = result.json()
        except ValueError:
            data = {"code":-1000}
        if -1 == data["code"] or -101 == data["code"]:
            return False
        return True

    def sendExportSuccess(self, id, downloadUrl):
        baseAddress = "http://" + self._ip + ":" + self._port
        requests.post(
            url=baseAddress + "/pl/communicate/worker-finish",
            json={"params":{"taskSettingId":int(id),"process":1,"downloadAddress":downloadUrl}},
            headers={"host": self._host},
            auth=(self._authUser,self._password)
        )

    def sendCancelSuccess(self, id):
        baseAddress = "http://" + self._ip + ":" + self._port
        requests.post(
            url=baseAddress + "/pl/communicate/worker-finish",
            json={"params":{"taskSettingId":int(id),"process":0,"downloadAddress":""}},
            headers={"host": self._host},
            auth=(self._authUser,self._password)
        )

    def prepareFloder(self):
        newUniqFloder = settings.EXPORT_TMP_FLODER + os.sep + uuid.uuid1().hex
        if not os.path.isdir(newUniqFloder):
            os.makedirs(newUniqFloder)
        if not os.path.isdir(newUniqFloder):
            self.stdout.write(self.style.ERROR("创建目录失败" + newUniqFloder))
            return False
        self._floder = newUniqFloder
        return True

    def cleanFloder(self):
        shutil.rmtree(self._floder)

    def queryString(self, queryString, startTime, endTime):
        """获取查询的语句"""
        queryTime = "[" + getTimeformate(startTime) + " TO " + getTimeformate(endTime) + "]"
        if "" == queryString or queryString is None:
            return "@timestamp:" + queryTime + " OR timestamp:" + queryTime
        else:
            return queryString + " AND (@timestamp:" + queryTime + " OR timestamp:" + queryTime + ")"

