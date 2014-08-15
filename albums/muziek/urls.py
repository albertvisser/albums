from django.conf.urls import *

urlpatterns = patterns('albums.muziek.views',
    (r'^$', 'index'),
    (r'^(?P<soort>(album|live))/select/$', 'select'),
    (r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<sortorder>\w+)/$',
        'select'),
    (r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'select'),
    (r'^(?P<soort>(album|live))/act/(?P<item>\d+)/$', 'sel_detail'),

    (r'^(?P<soort>(album|live))/nieuw/$', 'nieuw'),
    (r'^(?P<soort>(album|live))/nieuw/(?P<artiest>\d+)/$', 'nieuw'),
    (r'^(?P<soort>(album|live))/nieuw/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'nieuw'),
    (r'^(?P<soort>(album|live))/add/$', 'wijzig'),

    (r'^(?P<soort>(album|live))/(?P<item>\d+)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/(?P<keuze>\w+)/'
        '(?P<selitem>\w+)/(?P<sortorder>\w+)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>update)/$', 'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>update)/(?P<keuze>\w+)/'
        '(?P<selitem>\w+)/(?P<sortorder>\w+)/$', 'wijzig'),

    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/nieuw/$',
        'nieuw'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/add/$',
        'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
        '(?P<actie>edit)/$',  'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/all/'
        '(?P<actie>edit)/(?P<keuze>\w+)/(?P<selitem>\w+)/(?P<sortorder>\w+)/$',
        'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        '(?P<subitem>(\d+|all))/(?P<actie>update)/$',  'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        '(?P<subitem>(\d+|all))/(?P<actie>update)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$',  'wijzig'),
    (r'^(?P<type>(track|opname))/(?P<subitem>\d+)/edit/$', 'wijzig'),

    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'detail'),

    (r'^(?P<soort>artiest)/nieuw/$', 'nieuw'),
    (r'^(?P<soort>artiest)/add/$', 'wijzig'),
    (r'^artiest/(?P<actie>lijst)/$', 'artiest'),
    (r'^artiest/(?P<actie>lijst)/(?P<filter>\w+)/$', 'artiest'),
    (r'^(?P<soort>artiest)/(?P<item>(\d+|all))/update/$', 'wijzig'),
    ## (r'^artiest/(?P<actie>lijst)/edit/$',                                'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'detail'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
