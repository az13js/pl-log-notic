# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

class Command(BaseCommand):
    help = "后台导出 ES 数据工作进程"

    delay_sec = 1.0 # 延迟时间，秒

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("启动"))
        try:
            """测试命令，还未开发"""
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("停止执行"))
