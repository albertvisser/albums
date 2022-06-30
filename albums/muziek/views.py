"""Code to build pages to show
"""
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
import albums.muziek.models as my

# shouldn't these also be in the database?
s_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("titel", "3. Titel"),
            ("producer", "4. Producer"),
            ("credits", "5. Vermelding in Credits"),
            ("bezetting", "6. Vermelding in Bezetting"))
s_sorts = (("artiest", "Uitvoerende"),
           ("titel", "Titel"),
           ("jaar", "Jaar", "dflt"),
           ("geen", "Niets"))
l_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("locatie", "3. Locatie"),
            ("datum", "4. Datum"),
            ("bezetting", "5. Vermelding in Bezetting"))
l_sorts = (("artiest", "Uitvoerende"),
           ("locatie", "Locatie/datum", "dflt"),
           ("geen", "Niets"))
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


def index(request):
    """Prepare to show start page
    """
    return render(request, 'muziek/start.html', {
        "actlist": my.Act.objects.all().order_by('last_name'),
        "s_keuzes": s_keuzes,
        "s_sorts": s_sorts,
        "l_keuzes": l_keuzes,
        "l_sorts": l_sorts})


def select(request, soort="", keuze="", sortorder="", selitem=""):
    """Prepare Selection Page
    """
    postdict = request.GET
    if soort == 'album':
        info_dict = get_infodict_for_album(postdict, keuze, soort, selitem, sortorder)
    elif soort == 'live':
        info_dict = get_infodict_for_concert(postdict, keuze, soort, selitem, sortorder)
    else:
        info_dict = {"meld": 'Albumtype kon niet bepaald worden'}
    return render(request, 'muziek/select.html', info_dict)


def sel_detail(request, soort="", item=""):
    "snel naar een ander album van dezelfde artiest"
    postdict = request.GET
    return HttpResponseRedirect("/muziek/%s/%s/%s/%s/%s/" % (soort,
                                                             postdict["selAlbum"],
                                                             postdict['keuze'],
                                                             postdict['selitem'],
                                                             postdict['sortorder']))


def detail(request, soort="", keuze="", selitem="", sortorder="", item="", type="",
           actie=""):
    """Detailgegevens van een album
    """
    info_dict = {}
    album = my.Album.objects.get(pk=item)
    act_id = album.artist.id
    act_list = my.Album.objects.filter(artist=act_id)
    info_dict["track_list"] = album.tracks.all().order_by('volgnr')
    info_dict["opn_list"] = album.opnames.all()
    info_dict["album"] = album
    info_dict["soort"] = soort
    info_dict["keuze"] = keuze
    info_dict["selitem"] = selitem
    info_dict["sortorder"] = sortorder
    info_dict["o_soort"] = o_soort
    info_dict["o_oms"] = o_oms
    info_dict["act_id"] = act_id
    info_dict["type"] = type
    info_dict["actie"] = actie
    info_dict["actlist"] = my.Act.objects.all().order_by('last_name')
    if soort == 'album':
        info_dict["kop"] = "Gegevens van album " + str(album)
        info_dict["act_list"] = act_list.exclude(label="")
    elif soort == 'live':
        info_dict["kop"] = "Gegevens van concert: " + str(album)
        info_dict["act_list"] = act_list.filter(label="")
    else:
        info_dict["meld"] = 'Albumtype kon niet bepaald worden'
    if actie == 'edit':
        info_dict["meld"] = "Ok, we gaan openzetten"
    else:
        info_dict["meld"] = '{} / {} / {}'.format(keuze, selitem, sortorder)
    return render(request, 'muziek/detail.html', info_dict)


# detail met edit -> edit
def edit(request, soort="", keuze="", selitem="", sortorder="", item="", type=""):
    "openzetten detailscherm album voor wijzigen"
    return detail(request, soort, keuze, selitem, sortorder, item, type, actie='edit')


# detail voor track/all (met edit) -> edit_tracks
def edit_tracks(request, soort="", keuze="", selitem="", sortorder="", item="", type=""):
    "openzetten detailscherm track voor wijzigen"
    return detail(request, soort, keuze, selitem, sortorder, item, type='track', actie='edit')


# detail voor opname/all (met edit) -> edit_recs
def edit_recs(request, soort="", keuze="", selitem="", sortorder="", item="", type=""):
    "openzetten detaischerm opname voor wijzigen"
    return detail(request, soort, keuze, selitem, sortorder, item, type='opname', actie='edit')


def list_artists(request, soort="", actie="", filter=""):
    """toon een lijst met my.Act items
    """
    return render(request, 'muziek/artiesten.html',
                  {"artiesten": my.Act.objects.all().filter(
                      last_name__contains='{}'.format(filter)).order_by('last_name'),
                   "filter": filter})


# nieuw -> new
def new(request, soort="", item="", type="", artiest="", keuze="",
          selitem="", sortorder=""):
    """opvoeren van een album of artiest
    """
    data = {"kop": soort.join(("nieuwe ", " opname opvoeren")),
            "soort": soort,
            "keuze": keuze,
            "selitem": selitem,
            "sortorder": sortorder}
    data["nieuw"] = True
    if type in ('track', 'opname'):
        data["kop"] = type.join(("nieuw(e) ", " opvoeren"))
        album = my.Album.objects.get(id=item)
        aantal = album.tracks.count()
        data["album"] = album
        if type == "track":
            data["volgnr"] = str(aantal + 1)
            return render(request, "muziek/track.html", data)
        data["o_soort"] = o_soort
        return render(request, "muziek/opname.html", data)
    data["actie"] = "edit"
    if keuze == 'artiest':
        artiest = selitem
    elif keuze:
        data[keuze] = selitem
    data["act_id"] = int(artiest) if artiest else 0
    # eigenlijk moet hier voorzien gaan worden in andere mogelijkheden
    data["actlist"] = my.Act.objects.all().order_by('last_name')
    return render(request, 'muziek/detail.html', data)

# nieuw voor track -> new_track
def new_track(request, soort="", item="", type="", artiest="", keuze="",
          selitem="", sortorder=""):
    "openzetten track details voor opvoeren nieuw track"
    return new(request, soort, item, "track", artiest, keuze, selitem, sortorder)

# nieuw voor opname -> new_rec
def new_rec(request, soort="", item="", type="", artiest="", keuze="",
          selitem="", sortorder=""):
    "openzetten opname details voor opvoeren nieuwe opname"
    return new(request, soort, item, "opname", artiest, keuze, selitem, sortorder)


def new_artist(request, soort=''):
    # data["artiesten"] = "lijst"
    # data["artiest"] = "nieuw"
    # artiest.html gebruikt geen variabelen
    # soort komt mee vanuit de urlconf
    return render(request, 'muziek/artiest.html')  # , data)


# wijzig -> update
def update(request, soort="", item="", type="", subitem="", keuze="", selitem="",
           sortorder=""):
    """wijzigen van een album, track, opname of artiest
    """
    postdict = request.POST
    keuze = keuze or postdict.get('keuze', '')
    # if not keuze and 'keuze' in postdict:
    #     keuze = postdict['keuze']
    selitem = selitem or postdict.get('selitem', '')
    # if not selitem and 'selitem' in postdict:
    #     selitem = postdict['selitem']
    sortorder = sortorder or postdict.get('sortorder', '')
    # if not sortorder and 'sortorder' in postdict:
    #     sortorder = postdict['sortorder']
    if soort == "artiest":
        nextpage = do_artiest_update(postdict, item)
        return HttpResponseRedirect(nextpage)
    if type == "track":
        album = do_track_update(postdict, item, subitem)
    elif type == "opname":
        album = do_rec_update(postdict, item, subitem)
    elif soort in ("album", "live"):
        album = do_album_update(postdict, soort, item)
    if keuze:
        return HttpResponseRedirect("/muziek/%s/%s/%s/%s/%s/" % (soort, album.id, keuze,
                                                                 selitem, sortorder))
    return HttpResponseRedirect("/muziek/%s/%s/" % (soort, album.id))


# update voor track/all -> update_tracks
def update_tracks(request, soort="", item="", type="", subitem="", keuze="", selitem="",
                  sortorder=""):
    "bijwerken alle tracks in database in één keer"
    return update(request, soort=soort, item=item, type="track", subitem="all", keuze=keuze,
                  selitem=selitem, sortorder=sortorder)


# update voor track -> update_single_track
def update_single_track(request, soort="", item="", type="", subitem="", keuze="", selitem="",
                        sortorder=""):
    "bijwerken track in database"
    return update(request, soort=soort, item=item, type="track", subitem=subitem, keuze=keuze,
                  selitem=selitem, sortorder=sortorder)


# update voor opname/all -> update_recs
def update_recs(request, soort="", item="", type="", subitem="", keuze="", selitem="",
           sortorder=""):
    "bijwerken alle opnames in database in één keer"
    return update(request, soort, item, "opname", "all", keuze, selitem, sortorder)


# update voor opname -> update_single_rec
def update_single_rec(request, soort="", item="", type="", subitem="", keuze="", selitem="",
           sortorder=""):
    "bijwerken opname in database"
    return update(request, soort, item, "opname", subitem, keuze, selitem, sortorder)


def update_artists(request, soort="", item="", type="", subitem="", keuze="", selitem="",
           sortorder=""):
    "bijwerken alle artiesten in database in één keer"
    return update(request, soort, item, "artist", "all", keuze, selitem, sortorder)


def get_infodict_for_album(postdict, keuze, soort, selitem, sortorder):
    "ophalen variabelen voor scherm"
    meld = ''
    info_dict = {}
    if selitem:
        if keuze == s_keuzes[1][0]:
            sel_id = selitem
        else:
            zoektxt = selitem
    if 'selZoekS' in postdict:
        keuze = postdict['selZoekS']
    if 'selArtiest' in postdict:
        sel_id = postdict['selArtiest']
    if 'txtZoekS' in postdict:
        zoektxt = postdict['txtZoekS']
    if 'selSortS' in postdict:
        sortorder = postdict['selSortS']
    sel = my.Album.objects.exclude(label="")
    kop = "Lijst studio albums"
    altsel = 'live'
    altnaam = 'concert opnamen'
    altsort = sortorder
    if keuze == s_keuzes[0][0]:
        kop += " - selectie: alles"
        selitem = "alles"
    elif keuze == s_keuzes[1][0]:
        sel = sel.filter(artist=sel_id)
        kop += " - selectie: artiest '{}'".format(
            my.Act.objects.get(id=sel_id).get_name())
        selitem = sel_id
    elif keuze == s_keuzes[2][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += " - selectie: titel bevat '%s'" % zoektxt
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[3][0]:
        sel = sel.filter(produced_by__icontains=zoektxt)
        kop += " - selectie: produced_by bevat '%s'" % zoektxt
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[4][0]:
        sel = sel.filter(credits__icontains=zoektxt)
        kop += " - selectie: credits bevat '%s'" % zoektxt
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[5][0]:
        sel = sel.filter(bezetting__icontains=zoektxt)
        kop += " - selectie: bezetting bevat '%s'" % zoektxt
        selitem = zoektxt
    else:
        meld = 'Gekozen selectie kon niet uitgevoerd worden'
    if not meld:
        if sortorder == s_sorts[0][0]:
            sel = sel.order_by('artist')
            kop += " - gesorteerd op artiest"
        elif sortorder == s_sorts[1][0]:
            sel = sel.order_by('name')
            kop += " gesorteerd op titel"
            altsort = l_sorts[1][0]
        elif sortorder == s_sorts[2][0]:
            sel = sel.order_by('release_year')
            kop += " gesorteerd op jaar"
            altsort = l_sorts[1][0]
        elif sortorder == s_sorts[3][0]:
            pass
        else:
            meld = 'Gekozen selectie kon niet gesorteerd worden'
    if not meld:
        info_dict["kop"] = kop
        info_dict["keuze"] = keuze
        info_dict["soort"] = soort
        info_dict["sortorder"] = sortorder
        info_dict["selitem"] = selitem
        info_dict["actlist"] = my.Act.objects.all().order_by('last_name')
        if altsel:
            info_dict["altsel"] = altsel
            info_dict["altnaam"] = altnaam
            info_dict["altsort"] = altsort
        if len(sel) == 0:
            meld = "Geen albums gevonden"
        else:
            meld = "Kies een album uit de lijst:"
            info_dict["sel"] = sel
    info_dict["meld"] = meld
    return info_dict


def get_infodict_for_concert(postdict, keuze, soort, selitem, sortorder):
    "ophalen variabelen voor scherm"
    meld = ''
    info_dict = {}
    if selitem:
        if keuze == l_keuzes[1][0]:
            sel_id = selitem
        else:
            zoektxt = selitem
    if 'selZoekL' in postdict:
        keuze = postdict['selZoekL']
    if 'selArtiest' in postdict:
        sel_id = postdict['selArtiest']
    if 'txtZoekL' in postdict:
        zoektxt = postdict['txtZoekL']
    if 'selSortL' in postdict:
        sortorder = postdict['selSortL']
    sel = my.Album.objects.filter(label="")
    kop = "Lijst concert opnamen"
    altsel = 'album'
    altnaam = 'studio albums'
    altsort = sortorder
    if keuze == l_keuzes[0][0]:
        kop += " - selectie: alles"
        selitem = "alles"
    elif keuze == l_keuzes[1][0]:
        sel = sel.filter(artist=sel_id)
        kop += " - selectie: artiest '{}'".format(
            my.Act.objects.get(id=sel_id).get_name())
        selitem = sel_id
    elif keuze == l_keuzes[2][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += " - selectie: titel bevat locatie '%s'" % zoektxt
        selitem = zoektxt
        altsel = ''
    elif keuze == l_keuzes[3][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += " - selectie: titel bevat datum '%s'" % zoektxt
        selitem = zoektxt
        altsel = ''
    elif keuze == l_keuzes[4][0]:
        sel = sel.filter(bezetting__icontains=zoektxt)
        kop += " - selectie: bezetting bevat '%s'" % zoektxt
        selitem = zoektxt
    else:
        meld = 'Gekozen selectie kon niet uitgevoerd worden'
    if not meld:
        if sortorder == l_sorts[0][0]:
            sel = sel.order_by('artist')
            kop += " - gesorteerd op artiest"
        elif sortorder == l_sorts[1][0]:
            sel = sel.order_by('name')
            kop += " gesorteerd op locatie/datum"
            altsort = s_sorts[2][0]
        elif sortorder == l_sorts[2][0]:
            pass
        else:
            meld = 'Gekozen selectie kon niet gesorteerd worden'
    if not meld:
        info_dict["kop"] = kop
        info_dict["keuze"] = keuze
        info_dict["soort"] = soort
        info_dict["sortorder"] = sortorder
        info_dict["selitem"] = selitem
        info_dict["actlist"] = my.Act.objects.all().order_by('last_name')
        if altsel:
            info_dict["altsel"] = altsel
            info_dict["altnaam"] = altnaam
            info_dict["altsort"] = altsort
        if len(sel) == 0:
            meld = "Geen concerten gevonden"
        else:
            meld = "Kies een concertopname uit de lijst:"
            info_dict["sel"] = sel
    info_dict["meld"] = meld
    return info_dict


def do_artiest_update(postdict, item):
    "daadwerkelijk uitvoeren van de update"
    nextpage = "/muziek/artiest/lijst/"
    if not item:
        data = my.Act.objects.create()
        data.first_name = postdict['tNaam']
        data.last_name = postdict['tSort']
        data.save()
    elif item != 'all':
        data = my.Act.objects.get(pk=item)
        data.first_name = postdict['tNaam{}'.format(item)]
        data.last_name = postdict['tSort{}'.format(item)]
        data.save()
    else:
        all_artists = my.Act.objects.all().order_by('id')
        maxnum = int(all_artists.reverse()[0].id)
        all_keys = [x for x in postdict if x.startswith('tNaam') and len(x) > 5]
        for key in all_keys:
            act = my.Act.objects.get(pk=int(key[5:]))
            first_name_entered = postdict[key]
            last_name_entered = postdict['tSort{}'.format(key[5:])]
            modified = False
            if first_name_entered != act.first_name:
                act.first_name = first_name_entered
                modified = True
            if last_name_entered != act.last_name:
                act.last_name = last_name_entered
                modified = True
            if modified:
                act.save()
        f_names = postdict.getlist('tNaam')
        l_names = postdict.getlist('tSort')
        for ix, value in enumerate(l_names):
            maxnum += 1
            newact = my.Act.objects.create(id=maxnum,
                                           last_name=value,
                                           first_name=f_names[ix])
            newact.save()
        filter = postdict['filter']
        if filter:
            nextpage += filter + '/'
    return nextpage


def do_track_update(postdict, item, subitem):
    "daadwerkelijk uitvoeren van de update; geeft referentie naar het album terug"
    album = my.Album.objects.get(id=item)
    new_track = False
    if subitem == 'all':
        tracks = album.tracks.all().order_by('volgnr')
        tracks = list(tracks)
        tracks.reverse()
        maxnum = int(tracks[0].volgnr) if tracks else 0
        names = postdict.getlist('txtTrack0')
        authors = postdict.getlist('txtBy0')
        texts = postdict.getlist('txtCred0')
        for ix, value in enumerate(names):
            maxnum += 1
            newtrack = my.Song.objects.create(volgnr=maxnum,
                                              name=value,
                                              written_by=authors[ix],
                                              credits=texts[ix])
            newtrack.save()
            album.tracks.add(newtrack)
    elif subitem:
        tracks = [my.Song.objects.get(id=subitem)]
    else:
        new_track = True
        tracks = [my.Song.objects.create(id=postdict['tNr'])]
    for track in tracks:
        wijzig = False
        name = str(track.id)
        fieldname = 'tNaam' if new_track else "txtTrack" + name
        if postdict[fieldname] != track.name:
            track.name = postdict[fieldname]
            wijzig = True
        fieldname = 'tDoor' if new_track else "txtBy" + name
        if postdict[fieldname] != track.written_by:
            track.written_by = postdict[fieldname]
            wijzig = True
        fieldname = 'tCredits' if new_track else "txtCred" + name
        if postdict[fieldname] != track.credits:
            track.credits = postdict[fieldname]
            wijzig = True
        if wijzig:
            track.save()
            if new_track:
                album.tracks.add(track)
    return album


def do_rec_update(postdict, item, subitem):
    "daadwerkelijk uitvoeren van de update; geeft referentie naar het album terug"
    album = my.Album.objects.get(id=item)
    if subitem == 'all':
        opnames = list(album.opnames.all())
        types = postdict.getlist('selMed0')
        texts = postdict.getlist('txtOms0')
        for ix, value in enumerate(types):
            newopn = my.Opname.objects.create(type=value, oms=texts[ix])
            newopn.save()
            album.opnames.add(newopn)
    elif subitem:
        opnames = [my.Opname.objects.get(id=subitem)]
    else:
        opnames = [my.Opname()]
    selmed = postdict.getlist('selMed')
    txtoms = postdict.getlist("txtOms")
    for idx, opname in enumerate(opnames):
        wijzig = False
        if selmed[idx] != opname.type:
            opname.type = selmed[idx]
            wijzig = True
        if txtoms[idx] != opname.oms:
            opname.oms = txtoms[idx]
            wijzig = True
        if wijzig:
            opname.save()
            if not subitem:
                album.opnames.add(opname)
    return album


def do_album_update(postdict, soort, item):
    "daadwerkelijk uitvoeren van de update; geeft referentie naar het album terug"
    act = my.Act.objects.get(id=postdict["selArtiest"])
    if not item:
        album = my.Album.objects.create(artist=act, name=postdict["txtTitel"])
    else:
        album = my.Album.objects.get(id=item)
    wijzig = False
    if act != album.artist:
        album.artist = act
        wijzig = True
    if postdict["txtTitel"] != album.name:
        album.name = postdict["txtTitel"]
        wijzig = True
    if soort == "album":
        if postdict["txtLabel"] and postdict["txtLabel"] != album.label:
            album.label = postdict["txtLabel"]
            wijzig = True
        if postdict["txtJaar"] and postdict["txtJaar"] != album.release_year:
            album.release_year = postdict["txtJaar"]
            wijzig = True
    if postdict["txtProduced"] != album.produced_by:
        album.produced_by = postdict["txtProduced"]
        wijzig = True
    if postdict["txtCredits"] != album.credits:
        album.credits = postdict["txtCredits"]
        wijzig = True
    if postdict["txtBezetting"] != album.bezetting:
        album.bezetting = postdict["txtBezetting"]
        wijzig = True
    if postdict["txtAdditional"] != album.additional:
        album.additional = postdict["txtAdditional"]
        wijzig = True
    if wijzig:
        album.save()
    return album
