# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = "测试搜索"

    def handle(self, *args, **options):
        es = Elasticsearch(["127.0.0.1"], http_compress=True)
        if False == es.ping():
            self.stdout.write(self.style.ERROR("ping失败"))
            return False
        print(es.info())
        print(es.cluster.health())
        print(es.cluster.stats())


