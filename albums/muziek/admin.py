"""Register models with admin interface
"""
from albums.muziek.models import Act, Song, Opname, Album
from django.contrib import admin

admin.site.register(Act)  # , ActAdmin)
admin.site.register(Song)  # , SongAdmin)
admin.site.register(Opname)  # , OpnameAdmin)
admin.site.register(Album)  # , AlbumAdmin)
