"""smallmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import views
from smallmonitor.views import homepage, manager


urlpatterns = [
    url(r'^$', homepage),
    url(r'^manager/(?P<appid>[0-9]+)/$', manager),
    url(r'^api/groups/$', views.group_list),
    url(r'^api/groups/(?P<pk>[0-9]+)/$', views.group_detail),
    url(r'^api/apps/$', views.app_list),
    url(r'^api/app/(?P<pk>.+)/$', views.app_detail),
    url(r'^api/mangerapp/(?P<pk>[0-9]+)/$', views.manager_detail),
    url(r'^api/hosts/$', views.host_list),
    url(r'^api/hosts/(?P<pk>[0-9]+)/$', views.host_detail),
    url(r'^api/history/$', views.app_history_list),
    url(r'^api/statistics/(?P<pk>[0-9]+)$', views.app_statistics_list),
    url(r'^api/count/groups/$', views.count_groups_statistics_detail),
    url(r'^api/count/group/(?P<pk>[0-9]+)/$', views.count_group_statistics_detail),
]

