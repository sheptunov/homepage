# -*- coding: utf-8 -*-
"""homepage URL Configuration

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
from django.conf import settings
from portfolio.views import index, get_project


urlpatterns = [
    # Index
    url(r'^$', index, name='index'),

    # Ajax load project
    url(r'^project/$', get_project, name='get_project'),
    url(r'^project/(?P<project_slug>[a-z0-9-]+)$', get_project, name='get_project'),
    # Show raw html+css+js of choosen project
    url(r'^project/(?P<project_slug>[a-z0-9-]+)/(?P<project_mode>[a-z]+)/$', get_project, name='get_project'),

    # REST
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Define static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

