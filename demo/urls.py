"""demo URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import account

urlpatterns = [
    url(r'^$', include(account.users_urls)),
    url(r'^index/', include(account.users_urls)),
    url(r'^account/', include(account.users_urls)),
    url(r'^info/', include(account.info_urls)),
    url(r'^finance/', include(account.finance_urls)),
    url(r'^tender/', include(account.tender_urls)),
    url(r'^admin/', include(account.admin_urls)),
]
