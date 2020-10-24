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
    path('pl/task-test-es-link', api.task_test_es_link, name='task-test-es-link'), # 测试ES服务器连接
    path('pl/task-test-wxbot-address', api.task_test_wxbot_address, name='task-test-wxbot-address'), # 测试微信机器人地址
    path('pl/task-test-es-query', api.task_test_es_query, name='task-test-es-query'), # 测试 ES 查询方式
    path('pl/task-test-send-template', api.task_test_send_template, name='task-test-send-template'), # 测试发送模板
    path('pl/task-export-test', api.task_export_test, name='task-export-test') # 测试导出结果
]
