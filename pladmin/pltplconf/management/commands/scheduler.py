# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from pltplconf.models import Pljob
from django.utils import timezone
from datetime import timedelta
import time
from django.conf import settings
import importlib

class Command(BaseCommand):
    help = "开启定时任务"
    delay_sec = 1.0 # 间隔多少秒

    pipLineModules = [] # 流水线

    def handle(self, *args, **options):
        """间隔若干秒钟，持续执行定时任务"""
        self.stdout.write(self.style.SUCCESS("启动定时任务"))

        self.initModules()

        last_run_time = timezone.now()
        while True:
            try:
                exec_num = 0 # 计算job数量

                now_time = timezone.now() # 当前时间
                for job in Pljob.objects.filter(next_exec_time__lte=now_time):
                    exec_num = exec_num + 1
                    # 更新job数据
                    job.last_exec_time = timezone.now()
                    job.next_exec_time = job.last_exec_time + timedelta(seconds=job.delay_sec)
                    job.save()
                    # 执行job
                    self.handleJob(job)
                self.stdout.write(self.style.SUCCESS("执行了 " + str(exec_num) + " 个任务"))
                last_run_time = now_time # 记录最后一次执行的时间

                exec_time = timezone.now() - now_time # 计算一个 for 循环消耗的时间
                stop_time_second = self.delay_sec - exec_time.microseconds / 1000000.0
                if stop_time_second > 0:
                    self.stdout.write(self.style.SUCCESS("暂停 " + str(stop_time_second) + " 秒"))
                    time.sleep(stop_time_second) # 暂停一段时间，可能凑够self.delay_sec秒
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("停止执行"))
                exit(0)

    def handleJob(self, job):
        """处理任务的具体逻辑"""
        for pipline in self.pipLineModules:
            pipline.handle(job)

    def initModules(self):
        """实例化配置的流水线类"""
        for mod in settings.PL_PIPLINES:
            piplineClass = getattr(importlib.import_module(mod), mod.split('.')[-1])
            self.pipLineModules.append(piplineClass())




