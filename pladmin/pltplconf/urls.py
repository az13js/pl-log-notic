"""pltplconf URL Configuration

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 输出首页
    path('pl/task-list', views.task_list, name='task-list'), # 监控任务列表
    path('pl/task-add', views.task_add, name='task-add') # 添加新任务
]