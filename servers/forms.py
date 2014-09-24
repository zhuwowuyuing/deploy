__author__ = 'liangnaihua'

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'salt_MachineInfo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'index/', 'servers.views.index'),
    url(r'names/', 'servers.views.names'),
    url(r'serverlist/', 'servers.views.serverslist'),
)
