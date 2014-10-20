__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'status/create/$', 'assets.views.status_create'),
    url(r'status/list/$', 'assets.views.status_list'),
    url(r'status/edit/(?P<status>[^/]+)/$', 'assets.views.status_edit'),
    url(r'server/list/', 'assets.views.server_list'),
    url(r'server/create/', 'assets.views.server_create'),
    url(r'server/edit/(?P<asset>[^/]+)/$', 'assets.views.server_edit'),
    url(r'server/view/(?P<asset>[^/]+)/$', 'assets.views.server_view'),
    url(r'server/delete/(?P<asset>[^/]+)/$', 'assets.views.server_delete'),
    url(r'server/search/$', 'assets.views.server_search'),
    url(r'modlog/list/$', 'assets.views.modlog_list'),
)