# -*- coding: utf8 -*-

from django.db import models

class Pljob(models.Model):
    last_exec_time = models.DateTimeField("最后一次执行时间")
    next_exec_time = models.DateTimeField("下一次执行时间")
    delay_sec = models.IntegerField("延迟的时间（秒）")
    job_name = models.CharField("任务名称", max_length=100)
    es_query = models.CharField("查询命令", max_length=300, default="")
    es_query_num = models.IntegerField("查询数量", default=1)
    # system_type
    # 0 默认系统，SLOG，普通接口请求
    # 1 XLOG
    # 2 某品牌的错误日志监控
    system_type = models.IntegerField("系统类型", default=0)

    def __str__(self):
        if hasattr(self, "id"):
            return self.job_name + ",id=" + str(self.id) + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)
        return self.job_name + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)
