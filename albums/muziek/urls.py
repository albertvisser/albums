"""url configuration
"""
from django.conf.urls import *

urlpatterns = patterns(
    'albums.muziek.views',
    url(r'^$', 'index'),

    url(r'^(?P<soort>(album|live))/select/$', 'select'),
    url(r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<sortorder>\w+)/$',
     'select'),
    url(r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<selitem>\w+)/'
     r'(?P<sortorder>\w+)/$', 'select'),
    url(r'^(?P<soort>(album|live))/act/(?P<item>\d+)/$', 'sel_detail'),

    url(r'^(?P<soort>(album|live))/nieuw/$', 'nieuw'),
    url(r'^(?P<soort>(album|live))/nieuw/(?P<artiest>\d+)/$', 'nieuw'),
    url(r'^(?P<soort>(album|live))/nieuw/(?P<keuze>\w+)/(?P<selitem>\w+)/'
     r'(?P<sortorder>\w+)/$', 'nieuw'),
    url(r'^(?P<soort>(album|live))/add/$', 'wijzig'),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/$', 'detail'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/(?P<keuze>\w+)/'
     r'(?P<selitem>\w+)/(?P<sortorder>\w+)/$', 'detail'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/update/$', 'wijzig'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/update/(?P<keuze>\w+)/'
     r'(?P<selitem>\w+)/(?P<sortorder>\w+)/$', 'wijzig'),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/nieuw/$',
     'nieuw'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/add/$',
     'wijzig'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
     '(?P<actie>edit)/$', 'detail'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
     r'(?P<actie>edit)/(?P<keuze>\w+)/(?P<selitem>\w+)/(?P<sortorder>\w+)/$',
     'detail'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
     r'(?P<subitem>(\d+|all))/update/$', 'wijzig'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
     r'(?P<subitem>(\d+|all))/update/(?P<keuze>\w+)/(?P<selitem>\w+)/'
     r'(?P<sortorder>\w+)/$', 'wijzig'),
    # url(r'^(?P<type>(track|opname))/(?P<subitem>\d+)/edit/$', 'wijzig'),

    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
     r'(?P<sortorder>\w+)/$', 'detail'),

    url(r'^(?P<soort>artiest)/nieuw/$', 'nieuw'),
    url(r'^(?P<soort>artiest)/add/$', 'wijzig'),
    url(r'^artiest/(?P<actie>lijst)/$', 'artiest'),
    url(r'^artiest/(?P<actie>lijst)/(?P<filter>\w+)/$', 'artiest'),
    url(r'^(?P<soort>artiest)/(?P<item>(\d+|all))/update/$', 'wijzig'),
    # url(r'^artiest/(?P<actie>lijst)/edit/$',                                'wijzig'),
    url(r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
     r'(?P<sortorder>\w+)/$', 'detail'),

    # Uncomment this for admin:
    #     url(r'^admin/', include('django.contrib.admin.urls')),
)
