import os
import types
import pytest
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albums.settings')
django.setup()
from django.http import QueryDict
from albums.muziek import helpers
import albums.muziek.models as my

@pytest.mark.django_db
def test_get_infodict_for_index(monkeypatch, capsys):
    myact1 = my.Act.objects.create(last_name='us')
    myact2 = my.Act.objects.create(last_name='them')
    monkeypatch.setattr(helpers, 's_keuzes', 's_keuzes')
    monkeypatch.setattr(helpers, 's_sorts', 's_sorts')
    monkeypatch.setattr(helpers, 'l_keuzes', 'l_keuzes')
    monkeypatch.setattr(helpers, 'l_sorts', 'l_sorts')
    data = helpers.get_infodict_for_index()
    assert list(data['actlist']) == [myact2, myact1]
    assert (data["s_keuzes"], data["s_sorts"]) == ('s_keuzes', 's_sorts')
    assert (data["l_keuzes"], data["l_sorts"]) == ('l_keuzes', 'l_sorts')


@pytest.mark.django_db
def test_get_infodict_for_album(monkeypatch, capsys):
    assert helpers.get_infodict_for_album({}, '', '', '', '') == {
            'meld': 'Gekozen selectie kon niet worden uitgevoerd'}
    assert helpers.get_infodict_for_album({}, 'alles', '', '', '') == {
            'meld': 'Gekozen selectie kon niet worden gesorteerd'}
    data = helpers.get_infodict_for_album({}, 'alles', '', '', 'artiest')
    assert data['meld'] == 'Geen albums gevonden'

    artist = my.Act.objects.create(last_name='bladibla')
    artist2 = my.Act.objects.create(last_name='gargl')
    album1 = my.Album.objects.create(artist=artist, name='Number one', label='x', release_year='1',
                                     produced_by='naam', credits='tekt', bezetting='tekst')
    album2 = my.Album.objects.create(artist=artist, name='Number two', label='x', release_year=1,
                                     produced_by='nam', credits='Teksten', bezetting='TeKsT')
    album3 = my.Album.objects.create(artist=artist2, name='Number three', label='x', release_year=2,
                                     produced_by='Naam', credits='tekst', bezetting='ttekstt')
    album4 = my.Album.objects.create(artist=artist, name='Number three', label='x', release_year=1,
                                     produced_by='naampje', credits='getekstde', bezetting='')
    data = helpers.get_infodict_for_album({}, 'artiest', 'album', '1', 'titel')
    assert data['kop'] == "Lijst studio albums - selectie: artiest 'bladibla' gesorteerd op titel"
    assert (data['keuze'], data['soort'], data['sortorder']) == ('artiest', 'album', 'titel')
    assert (data['selitem'], list(data['actlist'])) == ('1', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('live', 'concert opnamen',
                                                                  'locatie')
    assert list(data['sel']) == [album1, album4, album2]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({}, 'alles', 'x', '', 'geen')
    assert data['kop'] == "Lijst studio albums - selectie: alles - niet gesorteerd"
    assert (data['keuze'], data['soort'], data['sortorder']) == ('alles', 'x', 'geen')
    assert (data['selitem'], list(data['actlist'])) == ('alles', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('live', 'concert opnamen',
                                                                  'geen')
    assert list(data['sel']) == [album1, album2, album3, album4]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({}, 'titel', '', 'three', 'artiest')
    assert data['kop'] == ("Lijst studio albums - selectie: titel bevat 'three'"
                           " - gesorteerd op artiest")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('titel', '', 'artiest')
    assert (data['selitem'], list(data['actlist'])) == ('three', [artist, artist2])
    assert list(data['sel']) == [album4, album3]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({}, 'producer', '', 'naam', 'jaar')
    assert data['kop'] == ("Lijst studio albums - selectie: produced_by bevat 'naam'"
                           " gesorteerd op jaar")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('producer', '', 'jaar')
    assert (data['selitem'], list(data['actlist'])) == ('naam', [artist, artist2])
    assert list(data['sel']) == [album1, album4, album3]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({}, 'credits', '', 'tekst', 'jaar')
    assert data['kop'] == ("Lijst studio albums - selectie: credits bevat 'tekst'"
                           " gesorteerd op jaar")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('credits', '', 'jaar')
    assert (data['selitem'], list(data['actlist'])) == ('tekst', [artist, artist2])
    assert list(data['sel']) == [album2, album4, album3]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({}, 'bezetting', '', 'tekst', 'artiest')
    assert data['kop'] == ("Lijst studio albums - selectie: bezetting bevat 'tekst'"
                           " - gesorteerd op artiest")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('bezetting', '', 'artiest')
    assert (data['selitem'], list(data['actlist'])) == ('tekst', [artist, artist2])
    assert list(data['sel']) == [album1, album2, album3]
    assert data['meld'] == 'Kies een album uit de lijst:'

    data = helpers.get_infodict_for_album({'selZoekS': 'artiest', 'selArtiest': '1',
                                           'selSortS': 'titel'}, '', '', '', '')
    assert data['kop'] == "Lijst studio albums - selectie: artiest 'bladibla' gesorteerd op titel"
    assert (data['keuze'], data['soort'], data['sortorder']) == ('artiest', '', 'titel')
    assert (data['selitem'], list(data['actlist'])) == ('1', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('live', 'concert opnamen',
                                                                  'locatie')
    assert list(data['sel']) == [album1, album4, album2]
    assert data['meld'] == 'Kies een album uit de lijst:'

    # data = helpers.get_infodict_for_album({'selZoekS': 'alles', 'selSortS': 'geen'},
    #                                       '', '', '', '')
    data = helpers.get_infodict_for_album({'selZoekS': 'titel', 'txtZoekS': 'ber t',
                                           'selSortS': 'artiest'}, '', '', '', '')
    assert data['kop'] == ("Lijst studio albums - selectie: titel bevat 'ber t'"
                           " - gesorteerd op artiest")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('titel', '', 'artiest')
    assert (data['selitem'], list(data['actlist'])) == ('ber t', [artist, artist2])
    assert list(data['sel']) == [album2, album4, album3]
    assert data['meld'] == 'Kies een album uit de lijst:'


@pytest.mark.django_db
def test_get_infodict_for_concert(monkeypatch, capsys):
    assert helpers.get_infodict_for_concert({}, '', '', '', '') == {
            'meld': 'Gekozen selectie kon niet worden uitgevoerd'}
    assert helpers.get_infodict_for_concert({}, 'alles', '', '', '') == {
            'meld': 'Gekozen selectie kon niet worden gesorteerd'}
    data = helpers.get_infodict_for_concert({}, 'alles', '', '', 'artiest')
    assert data['meld'] == 'Geen concerten gevonden'

    artist = my.Act.objects.create(last_name='bladibla')
    artist2 = my.Act.objects.create(last_name='gargl')
    album1 = my.Album.objects.create(artist=artist, name='Ergens, ooit',
                                     bezetting='tekst')
    album2 = my.Album.objects.create(artist=artist, name='Ergens anders, eens',
                                     bezetting='TeKsT')
    album3 = my.Album.objects.create(artist=artist2, name='Hier, Nooit',
                                     bezetting='ttekstt')
    album4 = my.Album.objects.create(artist=artist, name='Nergens, altijd',
                                     bezetting='')
    data = helpers.get_infodict_for_concert({}, 'artiest', 'live', '1', 'locatie')
    assert data['kop'] == ("Lijst concert opnamen - selectie: artiest 'bladibla'"
                           " gesorteerd op locatie/datum")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('artiest', 'live', 'locatie')
    assert (data['selitem'], list(data['actlist'])) == ('1', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('album', 'studio albums',
                                                                  'jaar')
    assert list(data['sel']) == [album2, album1, album4]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'
    data = helpers.get_infodict_for_concert({}, 'alles', 'x', '', 'geen')
    assert data['kop'] == "Lijst concert opnamen - selectie: alles - niet gesorteerd"
    assert (data['keuze'], data['soort'], data['sortorder']) == ('alles', 'x', 'geen')
    assert (data['selitem'], list(data['actlist'])) == ('alles', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('album', 'studio albums',
                                                                  'geen')
    assert list(data['sel']) == [album1, album2, album3, album4]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'
    data = helpers.get_infodict_for_concert({}, 'locatie', '', 'ergens', 'artiest')
    assert data['kop'] == ("Lijst concert opnamen - selectie: titel bevat locatie 'ergens'"
                           " - gesorteerd op artiest")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('locatie', '', 'artiest')
    assert (data['selitem'], list(data['actlist'])) == ('ergens', [artist, artist2])
    assert list(data['sel']) == [album1, album2, album4]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'
    data = helpers.get_infodict_for_concert({}, 'datum', '', 'ooit', 'artiest')
    assert data['kop'] == ("Lijst concert opnamen - selectie: titel bevat datum 'ooit'"
                           " - gesorteerd op artiest")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('datum', '', 'artiest')
    assert (data['selitem'], list(data['actlist'])) == ('ooit', [artist, artist2])
    assert list(data['sel']) == [album1, album3]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'
    data = helpers.get_infodict_for_concert({}, 'bezetting', '', 'tekst', 'locatie')
    assert data['kop'] == ("Lijst concert opnamen - selectie: bezetting bevat 'tekst'"
                           " gesorteerd op locatie/datum")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('bezetting', '', 'locatie')
    assert (data['selitem'], list(data['actlist'])) == ('tekst', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('album', 'studio albums',
                                                                  'jaar')
    assert list(data['sel']) == [album2, album1, album3]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'

    data = helpers.get_infodict_for_concert({'selZoekL': 'artiest', 'selArtiest': '1',
                                             'selSortL': 'locatie'}, '', '', '', '')
    assert data['kop'] == ("Lijst concert opnamen - selectie: artiest 'bladibla'"
                           " gesorteerd op locatie/datum")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('artiest', '', 'locatie')
    assert (data['selitem'], list(data['actlist'])) == ('1', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('album', 'studio albums',
                                                                  'jaar')
    assert list(data['sel']) == [album2, album1, album4]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'
    # data = helpers.get_infodict_for_concert({'selZoekL': 'alles', 'selSortL': 'geen'},
    #                                         '', '', '', '')
    data = helpers.get_infodict_for_concert({'selZoekL': 'bezetting', 'txtZoekL': 'tekst',
                                             'selSortL': 'locatie'}, '', '', '', '')
    assert data['kop'] == ("Lijst concert opnamen - selectie: bezetting bevat 'tekst'"
                           " gesorteerd op locatie/datum")
    assert (data['keuze'], data['soort'], data['sortorder']) == ('bezetting', '', 'locatie')
    assert (data['selitem'], list(data['actlist'])) == ('tekst', [artist, artist2])
    assert (data['altsel'], data['altnaam'], data['altsort']) == ('album', 'studio albums',
                                                                  'jaar')
    assert list(data['sel']) == [album2, album1, album3]
    assert data['meld'] == 'Kies een concertopname uit de lijst:'


@pytest.mark.django_db
def test_get_infodict_for_detail(monkeypatch, capsys):
    # meerdere acts opvoeren
    artist = my.Act.objects.create(last_name='bladibla')
    artist2 = my.Act.objects.create(last_name='gargl')
    myalbum = my.Album.objects.create(artist=artist, name='Number one', label='x', release_year='1',
                                      produced_by='naam', credits='tekt', bezetting='tekst')
    myalbum2 = my.Album.objects.create(artist=artist, name='Number one', label='x', release_year='1',
                                      produced_by='naam', credits='tekt', bezetting='tekst')
    myconcert = my.Album.objects.create(artist=artist, name='Ergens, ooit', bezetting='tekst')
    track = my.Song.objects.create(volgnr=2, name="Name1")
    track2 = my.Song.objects.create(volgnr=1, name="Name2")
    opname = my.Opname.objects.create(type='x', oms='y')
    myalbum.tracks.add(track, track2)
    myalbum.opnames.add(opname)
    data = helpers.get_infodict_for_detail('album', 'x', 'y', 'z', myalbum.id, 'a', 'b')
    assert (data['act_id'], list(data['act_list']), data['actie']) == (1, [myalbum, myalbum2], 'b')
    assert (list(data['actlist']), data['album'], data['keuze']) == ([artist, artist2], myalbum, 'x')
    assert data['kop'] == 'Gegevens van album bladibla - Number one (x, 1)'
    assert (data['o_oms'], data['o_soort']) == (helpers.my.o_oms, helpers.my.o_soort)
    assert (list(data['opn_list']), data['selitem'], data['soort']) == ([opname], 'y', 'album')
    assert (data['sortorder'], list(data['track_list'])) == ('z', [track2, track])
    assert data['type'] == 'a'
    data = helpers.get_infodict_for_detail('live', 'x', 'y', 'z', myconcert.id, 'a', 'b')
    assert (data['act_id'], list(data['act_list']), data['actie']) == (1, [myconcert], 'b')
    assert (list(data['actlist']), data['album'], ) == ([artist, artist2], myconcert)
    assert (data['keuze'], data['kop']) == ('x', 'Gegevens van concert: bladibla - Ergens, ooit ')
    assert (data['o_oms'], data['o_soort']) == (helpers.my.o_oms, helpers.my.o_soort)
    assert (list(data['opn_list']), data['selitem'], data['soort']) == ([], 'y', 'live')
    assert (data['sortorder'], list(data['track_list']), data['type']) == ('z', [], 'a')
    data = helpers.get_infodict_for_detail('q', 'x', 'y', 'z', myalbum.id, 'a', 'b')
    assert (data['act_id'], data['actie']) == (1, 'b')
    assert (list(data['actlist']), data['album'], data['keuze']) == ([artist, artist2], myalbum, 'x')
    assert data['meld'] == 'Albumtype kon niet bepaald worden'
    assert (data['o_oms'], data['o_soort']) == (helpers.my.o_oms, helpers.my.o_soort)
    assert (list(data['opn_list']), data['selitem'], data['soort']) == ([opname], 'y', 'q')
    assert (data['sortorder'], list(data['track_list'])) == ('z', [track2, track])
    assert data['type'] == 'a'

@pytest.mark.django_db
def test_get_infodict_for_artists(monkeypatch, capsys):
    myact1 = my.Act.objects.create(last_name='een')
    myact2 = my.Act.objects.create(last_name='twee')
    myact3 = my.Act.objects.create(last_name='drie')
    data = helpers.get_infodict_for_artists('ee')
    assert list(data['artiesten']) == [myact1, myact2]
    assert data['filter'] == 'ee'

@pytest.mark.django_db
def test_get_infodict_for_new_item(monkeypatch, capsys):
    # varianten: type (3e arg) track, opname of anders
    #            als anders dan keuze (5e arg) artiest of anders (enig overblijvende is album)
    # track en opname worden (nog) niet gebruikt omdat ik het openzetten anders doe
    # namelijk met JQuery op het detailscherm
    # soort kan zoals gewoonlijk album of live zijn maar is niet zo interessant
    # item is het album id
    # ik weet niet of type bij artiest anders is dan bij album maar ook niet boeiend
    artist = my.Act.objects.create(last_name='bladibla')
    artist2 = my.Act.objects.create(last_name='gargl')
    data = helpers.get_infodict_for_new_item('xxx', 1, 'yyy', '1', 'qqq', 'rrr', 'sss')
    assert (data['kop'], data['soort']) == ('nieuwe xxx opname opvoeren', 'xxx')
    assert (data['keuze'], data['selitem'], data['sortorder']) == ('qqq', 'rrr', 'sss')
    assert (data['nieuw'], data['actie'], data['qqq']) == (True, 'edit', 'rrr')
    assert (data['act_id'], list(data['actlist'])) == (1, [artist, artist2])
    data = helpers.get_infodict_for_new_item('xxx', 1, 'yyy', '', 'qqq', 'rrr', 'sss')
    assert (data['kop'], data['soort']) == ('nieuwe xxx opname opvoeren', 'xxx')
    assert (data['keuze'], data['selitem'], data['sortorder']) == ('qqq', 'rrr', 'sss')
    assert (data['nieuw'], data['actie'], data['qqq']) == (True, 'edit', 'rrr')
    assert (data['act_id'], list(data['actlist'])) == (0, [artist, artist2])
    data = helpers.get_infodict_for_new_item('xxx', 1, 'yyy', 'zzz', 'artiest', '2', 'sss')
    assert (data['kop'], data['soort']) == ('nieuwe xxx opname opvoeren', 'xxx')
    assert (data['keuze'], data['selitem'], data['sortorder']) == ('artiest', '2', 'sss')
    assert (data['nieuw'], data['actie']) == (True, 'edit')
    assert (data['act_id'], list(data['actlist'])) == (2, [artist, artist2])

    myalbum = my.Album.objects.create(artist=artist, name='Number one', label='x')
    track = my.Song.objects.create(volgnr=2, name="Name1")
    opname = my.Opname.objects.create(type='x', oms='y')
    myalbum.tracks.add(track)
    myalbum.opnames.add(opname)
    data = helpers.get_infodict_for_new_item('xxx', 1, 'track', 'zzz', 'qqq', 'rrr', 'sss')
    assert (data['kop'], data['soort']) == ('nieuw(e) track opvoeren', 'xxx')
    assert (data['keuze'], data['selitem'], data['sortorder']) == ('qqq', 'rrr', 'sss')
    assert (data['nieuw'], data['album'], data['volgnr']) == (True, myalbum, '2')
    data = helpers.get_infodict_for_new_item('xxx', 1, 'opname', 'zzz', 'qqq', 'rrr', 'sss')
    assert (data['kop'], data['soort']) == ('nieuw(e) opname opvoeren', 'xxx')
    assert (data['keuze'], data['selitem'], data['sortorder']) == ('qqq', 'rrr', 'sss')
    assert (data['nieuw'], data['album'], data['o_soort']) == (True, myalbum, helpers.my.o_soort)

@pytest.mark.django_db
def test_do_artiest_update(monkeypatch, capsys):
    name, surname = 'Albert', 'Visser'
    vervolg = '/muziek/artiest/lijst/'
    assert len(my.Act.objects.filter(first_name=name, last_name=surname)) == 0
    assert helpers.do_artiest_update({'tNaam': name, 'tSort': surname}, '') == vervolg
    assert len(my.Act.objects.filter(first_name=name, last_name=surname)) == 1
    artist = my.Act.objects.filter(first_name=name, last_name=surname).get()
    x = artist.id
    assert helpers.do_artiest_update({f'tNaam{x}': surname, f'tSort{x}': name}, x) == vervolg
    assert len(my.Act.objects.filter(first_name=name, last_name=surname)) == 0
    assert len(my.Act.objects.filter(first_name=surname, last_name=name)) == 1
    artist2 = my.Act.objects.create(first_name='same', last_name='other')
    artist3 = my.Act.objects.create(first_name='change', last_name='me')
    artist4 = my.Act.objects.create(first_name='no', last_name='changes')
    assert len(my.Act.objects.all()) == 4
    postdict = QueryDict(mutable=True)
    postdict.update({'tNaam00001': name, 'tSort00001': surname,
                     'tNaam00002': 'the', 'tSort00002': 'other',
                     'tNaam00003': 'change', 'tSort00003': 'places',
                     'tNaam00004': 'no', 'tSort00004': 'changes',
                     'filter': 'pass'})
    postdict.setlist('tNaam', ['new', ''])
    postdict.setlist('tSort', ['item', 'also_new'])
    request = types.SimpleNamespace(POST=postdict)

    assert helpers.do_artiest_update(postdict, 'all') == vervolg + 'pass/'
    artists = list(my.Act.objects.all())
    assert len(artists) == 6
    assert (artists[0].first_name, artists[0].last_name) == ('Albert', 'Visser')
    assert (artists[1].first_name, artists[1].last_name) == ('the', 'other')
    assert (artists[2].first_name, artists[2].last_name) == ('change', 'places')
    assert (artists[3].first_name, artists[3].last_name) == ('no', 'changes')
    assert (artists[4].first_name, artists[4].last_name) == ('new', 'item')
    assert (artists[5].first_name, artists[5].last_name) == ('', 'also_new')


@pytest.mark.django_db
def test_do_track_update(monkeypatch, capsys):
    myact = my.Act.objects.create(first_name='the', last_name='Others')
    myalbum = my.Album.objects.create(artist=myact, name='Something Completely Different')
    track1 = my.Song.objects.create(volgnr=1, name="And Now...")
    track2 = my.Song.objects.create(volgnr=2, name="It's...")
    myalbum.tracks.add(track1, track2)
    postdict = {'txtTrack2': 'The Larch!', 'txtBy2': '', 'txtCred2': ''}
    assert helpers.do_track_update(postdict, myalbum.id, track2.id) == myalbum
    data = myalbum.tracks.get(volgnr=2)
    assert (data.name, data.written_by, data.credits) == ('The Larch!', '', '')
    postdict = {'tNr': '3', 'tNaam': 'Norwegian Blue', 'tDoor': 'Monty Python',
                'tCredits': 'Beautiful Plumage'}
    assert helpers.do_track_update(postdict, myalbum.id, '') == myalbum
    data = list(myalbum.tracks.all())[-1]
    assert (data.name, data.written_by, data.credits) == ('Norwegian Blue', 'Monty Python',
                                                          'Beautiful Plumage')
    postdict = QueryDict(mutable=True)
    postdict.update({'txtTrack1': 'And now...', 'txtBy1': 'A. Larch', 'txtCred1': 'Yes',
                     'txtTrack2': "It's...", 'txtBy2': 'It is back', 'txtCred2': '',
                     'txtTrack3': 'Norwegian Blue', 'txtBy3': 'Monty Python',
                     'txtCred3': 'Beautiful Plumage'})
    postdict.setlist('txtTrack0', ['Norwegian Wood', 'x'])
    postdict.setlist('txtBy0', ['The Beatles', 'y'])
    postdict.setlist('txtCred0', ['This bird has flown', 'z'])
    assert helpers.do_track_update(postdict, myalbum.id, 'all') == myalbum
    data = list(myalbum.tracks.all())
    assert len(data) == 5
    assert (data[0].volgnr, data[0].name, data[0].written_by, data[0].credits) == (
            1, 'And now...', 'A. Larch', 'Yes')
    assert (data[1].volgnr, data[1].name, data[1].written_by, data[1].credits) == (
            2, "It's...", 'It is back', '')
    assert (data[2].volgnr, data[2].name, data[2].written_by, data[2].credits) == (
            3, 'Norwegian Blue', 'Monty Python', 'Beautiful Plumage')
    assert (data[3].volgnr, data[3].name, data[3].written_by, data[3].credits) == (
            4, 'Norwegian Wood', 'The Beatles', 'This bird has flown')
    assert (data[4].volgnr, data[4].name, data[4].written_by, data[4].credits) == (
            5, 'x', 'y', 'z')


@pytest.mark.django_db
def test_do_rec_update(monkeypatch, capsys):
    myact = my.Act.objects.create(first_name='the', last_name='Others')
    myalbum = my.Album.objects.create(artist=myact, name='Something Completely Different')
    opname1 = my.Opname.objects.create(type='xxx', oms='yyyyyyyy')
    opname2 = my.Opname.objects.create(type='aaa', oms='bbbbbbbb')
    myalbum.opnames.add(opname1, opname2)
    postdict = QueryDict(mutable=True)
    postdict.setlist('selMed', ['Xxx'])
    postdict.setlist('txtOms', ['Yyyyyyyy'])
    assert helpers.do_rec_update(postdict, myalbum.id, opname1.id) == myalbum
    data = list(myalbum.opnames.all())
    assert len(data) == 2
    assert (data[0].type, data[0].oms) == ('Xxx', 'Yyyyyyyy')

    postdict = QueryDict(mutable=True)
    postdict.setlist('selMed', ['qqq'])
    postdict.setlist('txtOms', ['rrrrrrrr'])
    assert helpers.do_rec_update(postdict, myalbum.id, '') == myalbum
    data = list(myalbum.opnames.all())
    assert len(data) == 3
    assert (data[-1].type, data[-1].oms) == ('qqq', 'rrrrrrrr')

    postdict = QueryDict(mutable=True)
    postdict.setlist('selMed', ['xxx', 'aaa', 'qqq'])
    postdict.setlist('txtOms', ['yyyyyyyy', 'bbbbbbbb', 'rrrrrrrr'])
    postdict.setlist('selMed0', ['012', 'abc'])
    postdict.setlist('txtOms0', ['34567890', 'defghijk'])
    assert helpers.do_rec_update(postdict, myalbum.id, 'all') == myalbum
    data = list(myalbum.opnames.all())
    assert len(data) == 5
    assert (data[0].type, data[0].oms) == ('xxx', 'yyyyyyyy')
    assert (data[1].type, data[1].oms) == ('aaa', 'bbbbbbbb')
    assert (data[2].type, data[2].oms) == ('qqq', 'rrrrrrrr')
    assert (data[3].type, data[3].oms) == ('012', '34567890')
    assert (data[4].type, data[4].oms) == ('abc', 'defghijk')


@pytest.mark.django_db
def test_do_album_update(monkeypatch, capsys):
    act1 = my.Act.objects.create(last_name='chachacha')
    act2 = my.Act.objects.create(last_name='nobody')
    postdict = {'selArtiest': act1.id, 'txtTitel': 'My Album', 'txtLabel': 'X', 'txtJaar': 1900,
                'txtProduced': 'me', 'txtCredits': 'all my own work', 'txtBezetting': 'just me',
                'txtAdditional': "No, that's all"}
    data = helpers.do_album_update(postdict, 'album', '')
    assert (data.artist, data.name, data.label) == (act1, 'My Album', 'X')
    assert (data.release_year, data.produced_by, data.credits) == (1900, 'me', 'all my own work')
    assert (data.bezetting, data.additional) == ('just me', "No, that's all")
    postdict = {'selArtiest': act2.id, 'txtTitel': 'My Album!', 'txtLabel': 'X', 'txtJaar': 1900,
                'txtProduced': 'me', 'txtCredits': 'all my own work', 'txtBezetting': 'just me',
                'txtAdditional': "No, that's all"}
    data = helpers.do_album_update(postdict, 'album', data.id)
    assert (data.artist, data.name, data.label) == (act2, 'My Album!', 'X')
    assert (data.release_year, data.produced_by, data.credits) == (1900, 'me', 'all my own work')
    assert (data.bezetting, data.additional) == ('just me', "No, that's all")
