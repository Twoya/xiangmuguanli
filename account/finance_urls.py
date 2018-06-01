# -*- coding: utf-8 -*-

from account import views, finance_views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # admin
    url(r'^summary(&page=\w+)?', finance_views.summary, name='summary'),
    # url(r'^new$', users_views.new, name='new'),
    # url(r'^edit(&page=\w+)?', info_views.edit, name='edit'),
    url(r'^process(&id=\w+)?(&page=\w+)?', finance_views.process, name='process'),
    # url(r'^stop(&id=\w+)?(&page=\w+)?', users_views.stop, name='stop'),
    url(r'^evaluation(&id=\w+)?(&page=\w+)?', finance_views.evaluation, name='evaluation'),
    url(r'^finance(&id=\w+)?(&page=\w+)?', finance_views.finance, name='finance'),
    url(r'^detail(&id=\w+)?(&page=\w+)?', finance_views.detail, name='detail'),
    url(r'^files(&id=\w+)?(&page=\w+)?', finance_views.files, name='files'),
    # url(r'^user', users_views.user, name='user'),
]
