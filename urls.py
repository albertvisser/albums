from django.conf.urls.defaults import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',        'pythoneer.views.index'),
    (r'^files/',   'pythoneer.views.viewdoc'),
    (r'^muziek/',  include('pythoneer.muziek.urls')),
    (r'^doctool/', include('pythoneer.doctool.urls')),


    # Uncomment this for admin:
    (r'^admin/(.*)', admin.site.root),
)
