"""Url configuration on project level
"""
from django.urls import include, path
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = [
    path('', views.index),
    path('files/', views.viewdoc),
    path('muziek/', include('albums.muziek.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
]
