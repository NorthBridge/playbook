"""playbook URL Configuration

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
from django.contrib.auth.views import login, logout
from django.conf.urls import include, url
from django.contrib import admin
from .core import views

urlpatterns = [
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^playbook/$', views.index, name='index'),
    url(r'^playbook/backlog/', include('playbook.apps.backlog.urls')),
    url(r'^playbook/core/', include('playbook.apps.core.urls')),
    url(r'^admin/', include(admin.site.urls)),
]