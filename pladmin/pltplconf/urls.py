"""pltplconf URL Configuration

"""
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'), # 输出首页
    path('pl/task-list', api.task_list, name='task-list'), # 监控任务列表
    path('pl/task-add', api.task_add, name='task-add'), # 添加新任务
    path('pl/task-delete', api.task_delete, name='task-delete'), # 删除指定任务
    path('pl/task-set-status', api.task_set_status, name='task-set-status'), # 修改任务开关状态
    path('pl/task-info', api.task_info, name='task-info'), # 获取任务信息
    path('pl/task-save-info', api.task_save_info, name='task-save-info'), # 保存任务信息
    path('pl/task-test-es-link', api.task_test_es_link, name='task-test-es-link') # 测试ES服务器连接
]
