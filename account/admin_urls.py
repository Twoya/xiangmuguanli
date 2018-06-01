# -*- coding: utf-8 -*-

from account import views, admin_views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # admin
    url(r'^summary(&page=\w+)?', admin_views.summary, name='summary'),
    url(r'^edit(&page=\w+)?', admin_views.edit, name='edit'),
    url(r'^process(&id=\w+)?(&page=\w+)?', admin_views.process, name='process'),
    url(r'^check(&id=\w+)?(&page=\w+)?', admin_views.check, name='check'),
    url(r'^edit(&id=\w+)?(&page=\w+)?', admin_views.edit, name='edit'),
    url(r'^capitalpool(&year=\w+)?', admin_views.capitalpool, name='capitalpool'),
    url(r'^evaluation(&id=\w+)?(&page=\w+)?', admin_views.evaluation, name='evaluation'),
    url(r'^finance(&id=\w+)?(&page=\w+)?', admin_views.finance, name='finance'),
    url(r'^detail(&id=\w+)?(&page=\w+)?', admin_views.detail, name='detail'),
    url(r'^tender(&id=\w+)?(&page=\w+)?', admin_views.tender, name='tend'),
    url(r'^files(&id=\w+)?(&page=\w+)?', admin_views.files, name='files'),

    # url(r'^user', users_views.user, name='user'),
]
