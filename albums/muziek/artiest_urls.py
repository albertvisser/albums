"""url configuration
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('nieuw/', views.nieuw),
    path('add/', views.wijzig),
    path('lijst/', views.artiest),
    path('lijst/<slug:filter>/', views.artiest),
    path('<int:item>/update/', views.wijzig),
    path('all/update/', views.wijzig),

    # Uncomment this for admin:
    #     url(r'^admin/', include('django.contrib.admin.urls')),
]
