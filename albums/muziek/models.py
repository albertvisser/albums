"""Data entities
"""
from django.db import models


class Act(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        result = self.last_name
        if self.first_name:
            result += ', ' + self.first_name
        return result

    def get_name(self):
        return " ".join((self.first_name, self.last_name)).strip()


class Song(models.Model):
    volgnr = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    written_by = models.CharField(max_length=50, blank=True)
    credits = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Opname(models.Model):
    type = models.CharField(max_length=10, blank=True)
    oms = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if self.type:
            h = self.type
            if self.oms:
                h = ": ".join((self.type, self.oms))
        else:
            h = self.oms
        return h


class Album(models.Model):
    artist = models.ForeignKey(Act, related_name='album')
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True)
    produced_by = models.CharField(max_length=50, blank=True)
    bezetting = models.TextField(blank=True)
    additional = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    tracks = models.ManyToManyField(Song, related_name='album', null=True)
    opnames = models.ManyToManyField(Opname, related_name='album')

    def __str__(self):
        ## h = self.name
        album = self.name
        hlp = ''
        if self.label:
            ## h = " (".join((h, self.label))
            ## if self.release_year:
                ## h = ", ".join((h, str(self.release_year)))
            ## h = "".join((h, ")"))
            hlp = self.label.replace('(unknown)', '')
        if self.release_year:
            year = str(self.release_year)
            hlp = ", ".join((hlp, year)) if hlp else year
        if hlp:
            hlp = hlp.join(('(', ')'))
        ## h = " - ".join((self.artist.get_name(), h))
        ## return h
        return "{} - {} {}".format(self.artist.get_name(), album, hlp)

## class AlbumList(models.Model):
    ## album = models.ForeignKey(Album, edit_inline=models.TABULAR, num_in_admin=1)
    ## track = models.ForeignKey(Song,core=True)
    ## def __str__(self):
        ## return ": ".join((str(self.album),str(self.track)))
    ## class Meta:
        ## order_with_respect_to = 'album'
