from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from pltplconf.models import Pljob
from django.utils import timezone

def index(request):
    return render(request, 'pltplconf/index.html')

def jsontest(request):
    result = []
    for x in range(3):
        job = Pljob(last_exec_time=timezone.now(),next_exec_time=timezone.now(),delay_sec=1,job_name="Test job name")
        job.save()
        result.append(job)
    return JsonResponse({'foo': 'bar'})


