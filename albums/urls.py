"""Url configuration on project level
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^files/', views.viewdoc),
    url(r'^muziek/', include('albums.muziek.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
