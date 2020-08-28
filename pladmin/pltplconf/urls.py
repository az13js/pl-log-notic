"""pltplconf URL Configuration

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jsontest', views.jsontest, name='jsontest'),
]
