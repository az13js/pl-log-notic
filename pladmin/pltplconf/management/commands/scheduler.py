# -*- coding: utf8 -*-

import redis
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, InterfaceError
from pltplconf.models import Pljob
from django.utils import timezone
from datetime import timedelta
import time
from django.conf import settings
import importlib
from django.db import close_old_connections

class Command(BaseCommand):
    help = "开启定时任务"
    delay_sec = 1.0 # 间隔多少秒

    pipLineModules = [] # 流水线

    def handle(self, *args, **options):
        """间隔若干秒钟，持续执行定时任务"""
        self.stdout.write(self.style.SUCCESS("启动定时任务"))
        self.initRedis()
        self.initModules()

        last_run_time = timezone.now()
        while True:
            try:
                exec_num = 0 # 计算job数量

                now_time = timezone.now() # 当前时间
                close_old_connections()
                for job in Pljob.objects.filter(next_exec_time__lte=now_time):
                    if not self.requireLock(job): # 在集群部署的时候，多个命令实例同时执行。这里通过锁的方式令一个job同时只能被一个命令实例执行
                        continue
                    exec_num = exec_num + 1
                    # 更新job数据
                    job.last_exec_time = now_time
                    job.next_exec_time = job.last_exec_time + timedelta(seconds=job.delay_sec)
                    close_old_connections()
                    job.save()
                    # 执行job
                    self.handleJob(job)
                self.stdout.write(self.style.SUCCESS("处理了 " + str(exec_num) + " 个任务"))
                last_run_time = now_time # 记录最后一次执行的时间

                exec_time = timezone.now() - now_time # 计算一个 for 循环消耗的时间
                stop_time_second = self.delay_sec - exec_time.microseconds / 1000000.0
                if stop_time_second > 0:
                    self.stdout.write(self.style.SUCCESS("暂停 " + str(stop_time_second) + " 秒"))
                    time.sleep(stop_time_second) # 暂停一段时间，可能凑够self.delay_sec秒
            except OperationalError as e:
                self.stdout.write(self.style.ERROR("循环处理任务失败，出现错误（OperationalError）：" + str(e)))
            except InterfaceError as e:
                self.stdout.write(self.style.ERROR("循环处理任务失败，出现错误（InterfaceError）：" + str(e)))
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("停止执行"))
                exit(0)

    def handleJob(self, job):
        """处理任务的具体逻辑"""
        for pipline in self.pipLineModules:
            try:
                pipline.handle(job)
            except Exception as e:
                self.stdout.write(self.style.ERROR("handleJob失败，出现异常。" + str(e)))

    def initModules(self):
        """实例化配置的流水线类"""
        for mod in settings.PL_PIPLINES:
            piplineClass = getattr(importlib.import_module(mod), mod.split('.')[-1])
            self.pipLineModules.append(piplineClass())

    def initRedis(self):
        """初始化和配置_redis实例"""
        if not hasattr(settings, "REDIS_SETTING"): # 如果用户从旧版本升级，那么配置文件不包含这个配置，这里得判断有没有这个新配置
            self._redis = None
            return
        if settings.REDIS_SETTING["host"] is None:
            self._redis = None
            return
        if settings.REDIS_SETTING["unix_socket_path"] is not None:
            self._redis = redis.Redis(unix_socket_path=settings.REDIS_SETTING["unix_socket_path"])
            return
        self._redis = redis.Redis(host=settings.REDIS_SETTING["host"], port=settings.REDIS_SETTING["port"], db=settings.REDIS_SETTING["db"])

    def requireLock(self, job):
        """ 获取一个锁 """
        if self._redis is None: # 如果单机器无须启用Redis，那么认为这个锁都获取成功
            return True
        try:
            return self._redis.set("pl_" + str(job.id), "1", ex=1, nx=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR("Redis操作异常：" + str(e)))
            self.initRedis()
        return False
