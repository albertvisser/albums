from django.db import models
import datetime

class Act(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return " ".join((self.first_name,self.last_name)).strip()
    ## class Admin:
        ## pass

class Song(models.Model):
    volgnr = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50) #, core=True)
    written_by = models.CharField(max_length=50, blank=True) #, core=True)
    credits = models.TextField(blank=True)
    def __unicode__(self):
        return self.name
    ## class Admin:
        ## pass

class Opname(models.Model):
    type = models.CharField(max_length=10, blank=True) #, core=True)
    oms = models.CharField(max_length=20, blank=True) # , core=True)
    def __unicode__(self):
        if self.type:
            h = self.type
            if self.oms:
                h = ": ".join((self.type,self.oms))
        else:
            h = self.oms
        return h
    ## class Admin:
        ## pass

class Album(models.Model):
    artist = models.ForeignKey(Act, related_name = 'album')
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True)
    produced_by = models.CharField(max_length=50, blank=True)
    bezetting = models.TextField(blank=True)
    additional = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    tracks = models.ManyToManyField(Song, related_name = 'album',null=True)
    opnames = models.ManyToManyField(Opname, related_name = 'album')
    def __unicode__(self):
        h = self.name
        if self.label:
            h = " (".join((h,self.label))
            if self.release_year:
                h = ", ".join((h,str(self.release_year)))
            h = "".join((h,")"))
        h = " - ".join((str(self.artist),h))
        return h # self.name
    ## class Admin:
        ## pass
        ## fields = (
            ## (None,{'fields' : ('artist', 'name')}),
        ## )

## class AlbumList(models.Model):
    ## album = models.ForeignKey(Album, edit_inline=models.TABULAR, num_in_admin=1)
    ## track = models.ForeignKey(Song,core=True)
    ## def __unicode__(self):
        ## return ": ".join((str(self.album),str(self.track)))
    ## class Meta:
        ## order_with_respect_to = 'album'
