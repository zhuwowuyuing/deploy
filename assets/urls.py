__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^status/create/$', 'assets.views.status_create'),
    url(r'^status/list/$', 'assets.views.status_list'),
    url(r'^status/edit/(?P<id>[^/]+)/$', 'assets.views.status_edit', name='status_edit'),
    url(r'^status/delete/(?P<id>[^/]+)/$', 'assets.views.status_del', name='status_del'),

    url(r'^type/create/$', 'assets.views.type_create'),
    url(r'^type/list/$', 'assets.views.type_list'),
    url(r'^type/edit/(?P<id>[^/]+)/$', 'assets.views.type_edit', name="type_edit"),
    url(r'^type/delete/(?P<id>[^/]+)/$', 'assets.views.type_del', name='type_del'),

    url(r'^subtype/create/$', 'assets.views.subtype_create'),
    url(r'^subtype/list/$', 'assets.views.subtype_list'),
    url(r'^subtype/edit/(?P<id>[^/]+)/$', 'assets.views.subtype_edit', name="subtype_edit"),
    url(r'^subtype/delete/(?P<id>[^/]+)/$', 'assets.views.subtype_del', name='subtype_del'),

    url(r'^server/list/', 'assets.views.server_list'),
    url(r'^server/create/', 'assets.views.server_create'),
    url(r'^server/edit/(?P<asset>[^/]+)/$', 'assets.views.server_edit'),
    url(r'^server/view/(?P<asset>[^/]+)/$', 'assets.views.server_view'),
    url(r'^server/delete/(?P<asset>[^/]+)/$', 'assets.views.server_delete'),
    url(r'^server/search/$', 'assets.views.server_search'),
    url(r'^modlog/list/$', 'assets.views.modlog_list'),
)
