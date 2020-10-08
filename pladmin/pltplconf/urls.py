"""pltplconf URL Configuration

"""
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'), # 输出首页
    path('pl/task-list', api.task_list, name='task-list'), # 监控任务列表
    path('pl/task-add', api.task_add, name='task-add'), # 添加新任务
    path('pl/task-delete', api.task_delete, name='task-delete') # 删除指定任务
]