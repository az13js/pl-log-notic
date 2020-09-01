# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = "测试搜索"

    def handle(self, *args, **options):
        es = Elasticsearch(
            [
                {"host": "127.0.0.1", "port": 80, "url_prefix": "elasticsearch"},
            ],
            headers={"kbn-version":"4.5.4","Host":"example.com.cn","User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/68.0"},
            timeout=5,
            http_compress=True
        )
        if False == es.ping():
            self.stdout.write(self.style.ERROR("ping失败"))
            return False
        print(es.info())
        print(es.cluster.health())
        print(es.cluster.stats())


