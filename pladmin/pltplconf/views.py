from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'pltplconf/index.html')

def jsontest(request):
    return JsonResponse({'foo': 'bar'})