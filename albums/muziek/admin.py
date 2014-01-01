from pythoneer.muziek.models import Act, Song, Opname, Album
from django.contrib import admin

class ActAdmin(admin.ModelAdmin):
    pass
admin.site.register(Act) # , ActAdmin)

class SongAdmin(admin.ModelAdmin):
    pass
admin.site.register(Song) # , SongAdmin)

class OpnameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Opname) # , OpnameAdmin)

class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album) # , AlbumAdmin)