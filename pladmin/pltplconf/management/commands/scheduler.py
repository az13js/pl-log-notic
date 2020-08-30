# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = "开启定时任务"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("启动定时任务"))
        while True:
            try:
                scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
                scheduler.add_jobstore(DjangoJobStore(), "default")
                scheduler.start()
            except OperationalError:
                self.stdout.write(self.style.ERROR("DB操作错误"))
                try:
                    scheduler.shutdown()
                except OperationalError:
                    self.stdout.write(self.style.ERROR("DB操作错误"))
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("停止定时器"))
                scheduler.shutdown()
                exit(0)
