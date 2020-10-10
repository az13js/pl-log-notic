from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def index(request):
    """输出首页，index.html"""
    return render(request, 'pltplconf/index.html')
