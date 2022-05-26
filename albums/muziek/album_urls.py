"""path configuration
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('select/', views.select),
    path('select/<slug:keuze>/<slug:sortorder>/', views.select),
    path('select/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.select),
    path('act/<int:item>/$', views.sel_detail),

    path('nieuw/$', views.nieuw),
    path('nieuw/<int:artiest>/$', views.nieuw),
    path('nieuw/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.nieuw),
    path('add/$', views.wijzig),

    path('<int:item>/$', views.detail),
    path('<int:item>/edit/$', views.detail),
    path('<int:item>/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.detail),
    path('<int:item>/update/$', views.wijzig),
    path('<int:item>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.wijzig),

    path('<int:item>/track/nieuw/$', views.nieuw),
    path('<int:item>/track/add/$', views.wijzig),
    path('<int:item>/track/all/edit/$', views.detail),
    path('<int:item>/track/all/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.detail),
    path('<int:item>/track/all/update/', views.wijzig),
    path('<int:item>/track/<int:subitem>/update/', views.wijzig),
    path('<int:item>/track/all/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.wijzig),
    path('<int:item>/track/<int:subitem>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.wijzig),

    path('<int:item>/opname/nieuw/$', views.nieuw),
    path('<int:item>/opname/add/$', views.wijzig),
    path('<int:item>/opname/all/edit/$', views.detail),
    path('<int:item>/opname/all/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.detail),
    path('<int:item>/opname/all/update/$', views.wijzig),
    path('<int:item>/opname/<int:subitem>(\d+|all))/update/', views.wijzig),
    path('<int:item>/opname/all/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.wijzig),
    path('<int:item>/opname/<int:subitem>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.wijzig),

    path('<int:item>/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.detail),
]
