from django.conf.urls.defaults import *

urlpatterns = patterns('pythoneer.muziek.views',
    (r'^$', 'index'),
    (r'^(?P<soort>(album|live))/select/$', 'select'),
    (r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<sortorder>\w+)/$',
        'select'),
    (r'^(?P<soort>(album|live))/select/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'select'),
    (r'^(?P<soort>(album|live))/act/(?P<item>\d+)/$', 'sel_detail'),
    (r'^(?P<soort>(album|live))/nieuw/$', 'nieuw'),
    (r'^(?P<soort>(album|live))/nieuw/(?P<artiest>\d+)$', 'nieuw'),
    (r'^(?P<soort>(album|live))/add/$', 'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>edit)/$', 'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<actie>update)/$', 'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/nieuw/$',
        'nieuw'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/add/$',
        'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        'all/(?P<actie>edit)/$',  'detail'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        '(?P<subitem>\d+)/(?P<actie>edit)/$',  'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<type>(track|opname))/'
        '(?P<subitem>(\d+|all))/(?P<actie>update)/$',  'wijzig'),
    (r'^(?P<type>(track|opname))/(?P<subitem>\d+)/edit/$', 'wijzig'),
    (r'^(?P<soort>artiest)/nieuw/$', 'nieuw'),
    (r'^(?P<soort>artiest)/add/$', 'wijzig'),
    (r'^artiest/(?P<actie>lijst)/$', 'artiest'),
    (r'^(?P<soort>artiest)/(?P<item>\d+)/edit/$', 'wijzig'),
    ## (r'^artiest/(?P<actie>lijst)/edit/$',                                'wijzig'),
    (r'^(?P<soort>(album|live))/(?P<item>\d+)/(?P<keuze>\w+)/(?P<selitem>\w+)/'
        '(?P<sortorder>\w+)/$', 'detail'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
