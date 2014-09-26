__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'names/', 'servers.views.names'),
    url(r'list/', 'servers.views.server_list'),
    url(r'view/(?P<hostname>[^/]+)/$', 'servers.views.server_view'),
    url(r'errors/', 'servers.views.server_errors'),
)