"""Url configuration on project level
"""
from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'albums.views.index'),
    (r'^files/', 'albums.views.viewdoc'),
    (r'^muziek/', include('albums.muziek.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
