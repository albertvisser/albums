"""path configuration
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('select/', views.select),
    path('select/<slug:keuze>/<slug:sortorder>/', views.select),
    path('select/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.select),
    path('act/<int:item>/', views.sel_detail),

    path('nieuw/', views.new),
    path('nieuw/<int:artiest>/', views.new),
    path('nieuw/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.new),
    path('add/', views.update),

    path('<int:item>/', views.detail),
    path('<int:item>/edit/', views.edit),
    path('<int:item>/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.edit),
    path('<int:item>/update/', views.update),
    path('<int:item>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.update),

    path('<int:item>/track/nieuw/', views.new_track),
    path('<int:item>/track/add/', views.update_single_track),
    path('<int:item>/track/all/edit/', views.edit_tracks),
    path('<int:item>/track/all/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.edit_tracks),
    path('<int:item>/track/all/update/', views.update_tracks),
    path('<int:item>/track/<int:subitem>/update/', views.update_single_track),
    path('<int:item>/track/all/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.update_tracks),
    path('<int:item>/track/<int:subitem>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.update_single_track),

    path('<int:item>/opname/nieuw/', views.new_rec),
    path('<int:item>/opname/add/', views.update_single_rec),
    path('<int:item>/opname/all/edit/', views.edit_recs),
    path('<int:item>/opname/all/edit/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.edit_recs),
    path('<int:item>/opname/all/update/', views.update_recs),
    path('<int:item>/opname/<int:subitem>/update/', views.update_single_rec),
    path('<int:item>/opname/all/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.update_recs),
    path('<int:item>/opname/<int:subitem>/update/<slug:keuze>/<slug:selitem>/<slug:sortorder>/',
        views.update_single_rec),

    # deze aan het eind anders slokt-ie andere urls op (bv. track/all/edit)
    path('<int:item>/<slug:keuze>/<slug:selitem>/<slug:sortorder>/', views.detail),
]
