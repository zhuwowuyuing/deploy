__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'names/', 'servers.views.names'),
    url(r'list/', 'servers.views.server_list'),
)