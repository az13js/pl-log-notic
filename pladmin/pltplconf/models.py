# -*- coding: utf8 -*-

from django.db import models

class Pljob(models.Model):
    last_exec_time = models.DateTimeField("最后一次执行时间")
    next_exec_time = models.DateTimeField("下一次执行时间")
    delay_sec = models.IntegerField("延迟的时间（秒）")
    job_name = models.CharField("任务名称", max_length=100)
    wx_address = models.URLField("消息通知地址", max_length=400)

    def __str__(self):
        if hasattr(self, "id"):
            return self.job_name + ",id=" + str(self.id) + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)
        return self.job_name + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)
