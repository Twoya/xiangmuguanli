# -*- coding: utf-8 -*-

from account import views, users_views, info_views
from django.conf.urls import url

urlpatterns = [
    # url(r'^logout/$', views.logout, name='logout'),
    # url(r'^check_failed/$', views.check_failed, name='check_failed'),  # 权限验证错误页面
    url(r'^$', views.index, name='index'),
    # account
    url(r'^summary(&page=\w+)?', users_views.summary, name='summary'),
    url(r'^new$', users_views.new, name='new'),
    url(r'^user_edit(&page=\w+)?', users_views.user_edit, name='user_edit'),
    url(r'^process(&id=\w+)?(&page=\w+)?', users_views.process, name='process'),
    url(r'^stop(&id=\w+)?(&page=\w+)?', users_views.stop, name='stop'),
    url(r'^evaluation(&id=\w+)?(&page=\w+)?', users_views.evaluation, name='e'),
    url(r'^finance(&id=\w+)?(&page=\w+)?', users_views.finance, name='finance'),
    url(r'^new_finance(&id=\w+)?(&page=\w+)?', users_views.new_finance, name='new_finance'),
    url(r'^files(&id=\w+)?(&page=\w+)?', users_views.files, name='files'),
    url(r'^user', users_views.user, name='user'),
]
