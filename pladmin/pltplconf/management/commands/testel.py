# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = "测试搜索"

    def handle(self, *args, **options):
        es = Elasticsearch(["http://127.0.0.1:8088/elasticsearch"],headers={"kbn-version":"4.5.4","Host":"example.com.cn","User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},timeout=20)
        #if False == es.ping():
        #    self.stdout.write(self.style.ERROR("ping失败"))
            #return False
        #print(es.info())
        print(es.cluster.health())
        #print(es.cluster.stats())


