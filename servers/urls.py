__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'names/', 'servers.views.names'),
    url(r'serverlist/', 'servers.views.serverlist'),
)