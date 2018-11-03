"""url configuration
"""
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),

    url(r'^(?P<soort>(album|live))/select/$', views.select),
    url(r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<sortorder>\w+)/$',
        views.select),
    url(r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        r'(?P<sortorder>\w+)/$', views.select),
    url(r'^(?P<soort>(album|live))/act/(?P<item>\d+)/$', views.sel_detail),

    url(r'^(?P<soort>(album|live))/nieuw/$', views.nieuw),
    url(r'^(?P<soort>(album|live))/nieuw/(?P<artiest>\d+)/$', views.nieuw),
    url(r'^(?P<soort>(album|live))/nieuw/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        r'(?P<sortorder>\w+)/$', views.nieuw),
    url(r'^(?P<soort>(album|live))/add/$', views.wijzig),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/$', views.detail),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/$', views.detail),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/(?P<keuze>\w+)/'
        r'(?P<selitem>\w+)/(?P<sortorder>\w+)/$', views.detail),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/update/$', views.wijzig),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/update/(?P<keuze>\w+)/'
        r'(?P<selitem>\w+)/(?P<sortorder>\w+)/$', views.wijzig),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/nieuw/$',
        views.nieuw),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/add/$',
        views.wijzig),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
        '(?P<actie>edit)/$', views.detail),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
        r'(?P<actie>edit)/(?P<keuze>\w+)/(?P<selitem>\w+)/(?P<sortorder>\w+)/$',
        views.detail),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        r'(?P<subitem>(\d+|all))/update/$', views.wijzig),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        r'(?P<subitem>(\d+|all))/update/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        r'(?P<sortorder>\w+)/$', views.wijzig),
    # url(r'^(?P<type>(track|opname))/(?P<subitem>\d+)/edit/$', views.wijzig),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        r'(?P<sortorder>\w+)/$', views.detail),

    url(r'^(?P<soort>artiest)/nieuw/$', views.nieuw),
    url(r'^(?P<soort>artiest)/add/$', views.wijzig),
    url(r'^artiest/(?P<actie>lijst)/$', views.artiest),
    url(r'^artiest/(?P<actie>lijst)/(?P<filter>\w+)/$', views.artiest),
    url(r'^(?P<soort>artiest)/(?P<item>(\d+|all))/update/$', views.wijzig),
    # url(r'^artiest/(?P<actie>lijst)/edit/$', views.wijzig),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        r'(?P<sortorder>\w+)/$', views.detail),

    # Uncomment this for admin:
    #     url(r'^admin/', include('django.contrib.admin.urls')),
]
