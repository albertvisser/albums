"""url configuration
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('album/', include('albums.muziek.album_urls'), {'soort': 'album'}),
    path('live/', include('albums.muziek.album_urls'), {'soort': 'live'}),
    path('artiest/', include('albums.muziek.artiest_urls'), {'soort': 'artiest'}),

    # Uncomment this for admin:
    #     url(r'^admin/', include('django.contrib.admin.urls')),
]
