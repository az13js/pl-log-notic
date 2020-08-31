# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = "测试搜索"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("命令开始执行"))
        es = Elasticsearch(["127.0.0.1"], http_compress=True)
        print(es.ping())
        print(es.info())
        print(es.cluster.health())
        print(es.cluster.stats())


