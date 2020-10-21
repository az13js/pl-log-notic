# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from pltplconf import api
from pltplconf.models import Pljob
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "后台导出 ES 数据工作进程"

    delay_sec = 1.0 # 延迟时间，秒

    def handle(self, *args, **options):
        # TODO 支持在后台大量地按照条件导出ES中的数据，并且提取信息，弄成CSV文件之类的
        self.stdout.write(self.style.SUCCESS("启动"))
        job = Pljob.objects.get(id=7)
        api.fixQuery(job, timezone.now() - timedelta(days=job.delay_sec), timezone.now())
        # es = Elasticsearch(
        #     [{"host": "127.0.0.1", "port": 8102}],
        #     timeout=30,
        #     http_compress=True,
        #     use_ssl=False,
        #     verify_certs=False
        # )
        # print(es.info())
