"""url configuration
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('nieuw/', views.new_artist),
    path('add/', views.update),
    path('lijst/', views.list_artists),
    path('lijst/<slug:filter>/', views.list_artists),
    path('<int:item>/update/', views.update),
    path('all/update/', views.update_artists),

    # Uncomment this for admin:
    #     url(r'^admin/', include('django.contrib.admin.urls')),
]
