from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# 定时任务操作
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

def my_job():
    fw = open("/tmp/xdebug.log", "w+")
    fw.write("RUN\n")
    fw.close()

def index(request):
    return render(request, 'pltplconf/index.html')

def jsontest(request):
    #scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        my_job,
        trigger=CronTrigger(second="*"),
        id="my_job",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
    #scheduler.shutdown()
    return JsonResponse({'foo': 'bar', 'jobs': str(scheduler.get_jobs())})