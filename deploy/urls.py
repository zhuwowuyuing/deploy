from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Deploy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^servers/', include('servers.urls')),
    url(r'^assets/', include('assets.urls')),
    url(r'^$', "servers.views.index"),
    url(r'^index/$', 'servers.views.index'),
)
