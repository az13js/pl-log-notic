# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from pltplconf.management.commands.Collectors.example import example

class Command(BaseCommand):
    help = "测试搜索"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(example().find()))


