# -*- coding: utf8 -*-

from django.db import models

class Pljob(models.Model):
    task_setting = models.OneToOneField("PlTaskSetting", on_delete=models.CASCADE)
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
    # 3 默认系统的错误日志监控
    # 4 默认系统推送消息时间监控
    # 5 关联 PlTaskSetting 的数据
    system_type = models.IntegerField("系统类型", default=0)

    def __str__(self):
        if hasattr(self, "id"):
            return self.job_name + ",id=" + str(self.id) + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)
        return self.job_name + ",最近更新" + str(self.last_exec_time) + ",下次更新" + str(self.next_exec_time)

"""
    任务配置表
新的任务使用这里的配置，旧的为了继续运行，暂时不删除。
"""
class PlTaskSetting(models.Model):
    task_name = models.CharField("任务名称", max_length=64, default="", unique=True)
    status = models.SmallIntegerField("状态(1:开,0:关)", default=0)
    es_host = models.CharField("ES 主机名", max_length=100, default="")
    es_ip = models.CharField("ES ip 地址", max_length=64, default="")
    es_sechma = models.CharField("ES 访问协议", max_length=6, default="http")
    compress = models.SmallIntegerField("压缩(1:开,0:关)", default=0)
    auth_user = models.CharField("ES 用户名", max_length=100, default="")
    auth_pwd = models.CharField("ES 密码", max_length=100, default="")
    query_string = models.CharField("查询条件", max_length=500, default="")
    query_type = models.CharField("查询类型", max_length=20, default="")
    wx_bot_addr = models.CharField("企业微信机器人地址", max_length=100, default="")
    template = models.TextField("推送文本", default="")
    placeholders = models.TextField("占位符JSON数组", default="")
    delay_sec = models.IntegerField("每隔多少秒查询一次 ES 服务器", default=1)
    push_min = models.IntegerField("查询到多少条结果触发推送", default=0)
    max_per_hour = models.FloatField("每小时推送限制", default=0.0)
    kbn_version = models.CharField("Kibana版本号", max_length=15, default="")
    url_prefix = models.CharField("前缀", max_length=15, default="elasticsearch")
    es_port = models.CharField("端口号", max_length=6, default="")

    def __str__(self):
        if hasattr(self, "id"):
            return "id=" + str(self.id) + ",任务名称" + self.task_name
        return "任务名称" + self.task_name

"""
    job推送记录
"""
class PlPushLog(models.Model):
    job_pri_key = models.IntegerField("Job主键ID", default=0, db_index=True)
    push_time = models.DateTimeField("推送时间", db_index=True)

    def __str__(self):
        return "JOBID=" + str(self.job_pri_key) + ",TIME=" + str(self.push_time)

class PlExportJob(models.Model):
    """导出ES数据任务"""

    task_setting_id = models.IntegerField("PlTaskSetting主键", unique=True)
    status = models.SmallIntegerField("状态(0无任务,1已提交,2运行中)", default=0)
    run_time = models.DateTimeField("开始运行的时间")
    req_stop = models.SmallIntegerField("请求停止任务？", default=0)
    process = models.FloatField("进度", default=0.0)
    worker_name = models.CharField("工作进程名称", max_length=50, default="")
    download_addr = models.CharField("文件下载地址", max_length=150, default="")
    task_setting_info = models.TextField("任务设置JSON", default="")
    export_setting_info = models.TextField("导出设置JSON", default="")

    def __str__(self):
        return "关联task_setting_id=" + str(self.task_setting_id) + ",状态=" + str(self.status)
