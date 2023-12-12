"""Data entities
"""
from django.db import models

o_soort = ('Cassette',
           'CD: Enkel',
           'CD: Dubbel',
           'Vinyl: 1LP',
           'Vinyl: 2LP',
           'Vinyl: 3LP',
           'Vinyl: single',
           'Vinyl: 12" single',
           'Tape',
           'MP3 directory',
           'Banshee music player',
           'Clementine music player')
o_oms = ('eigen doosje',
         'map A-E',
         'map F-S',
         'map T-Z',
         'map Live')


class Act(models.Model):
    """Gegevens uitvoerende artiest(en)
    """
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        result = self.last_name
        if self.first_name:
            result += ', ' + self.first_name
        return result

    def get_name(self):
        """geef naam terug zoals de gebruiker hem wil zien
        """
        return f"{self.first_name} {self.last_name}".strip()


class Song(models.Model):
    """Gegegens van een afzonderlijke song
    """
    volgnr = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    written_by = models.CharField(max_length=50, blank=True)
    credits = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Opname(models.Model):
    """Gegegens over een bepaalde vastlegging van een songs-verzameling
    """
    # is dit een sqlite "feature"? ondanks max_length 10 worden langere omschrijvingen (zie boven)
    # toch opgeslagen. In de admin webinterface wordt het maximum wel gerespecteerd
    # of is het toch een Django dingetje dat alleen bedoeld is als een input beperking die je kunt
    # gebruiken of niet?
    type = models.CharField(max_length=10, blank=True)
    oms = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if self.type:
            result = self.type
            if self.oms:
                result = f"{self.type}: {self.oms}"
        else:
            result = self.oms
        return result


class Album(models.Model):
    """Gegevens van een songs-verzameling (album of concert)
    """
    artist = models.ForeignKey(Act, related_name='album', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True)
    produced_by = models.CharField(max_length=50, blank=True)
    bezetting = models.TextField(blank=True)
    additional = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    tracks = models.ManyToManyField(Song, related_name='album')
    opnames = models.ManyToManyField(Opname, related_name='album')

    def __str__(self):
        album = self.name
        hlp = self.labelstr()
        if hlp:
            hlp = hlp.join(('(', ')'))
        return f"{self.artist.get_name()} - {album} {hlp}"

    def labelstr(self):
        """Geef label plus jaar terug (gescheiden door een komma)
        """
        hlp = ''
        if self.label:
            hlp = self.label.replace('(unknown)', '')
        if self.release_year:
            year = str(self.release_year)
            hlp = f"{hlp}, {year}" if hlp else year
        return hlp

## class AlbumList(models.Model):
    ## album = models.ForeignKey(Album, edit_inline=models.TABULAR, num_in_admin=1)
    ## track = models.ForeignKey(Song,core=True)
    ## def __str__(self):
        ## return ": ".join((str(self.album),str(self.track)))
    ## class Meta:
        ## order_with_respect_to = 'album'
