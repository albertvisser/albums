"""Code to build pages to show
"""
# from django.http import HttpResponseRedirect, Http404, HttpResponse
# from django.shortcuts import render
import albums.muziek.models as my

# shouldn't these also be in the database?
s_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("titel", "3. Tekst in Titel"),
            ("producer", "4. Tekst in Producer"),
            ("credits", "5. Tekst in Credits"),
            ("bezetting", "6. Tekst in Bezetting"))
s_sorts = (("artiest", "Uitvoerende"),
           ("titel", "Titel"),
           ("jaar", "Jaar", "dflt"),
           ("geen", "Niets"))
l_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("locatie", "3. Tekst in Locatie"),
            ("datum", "4. Tekst in Datum"),
            ("bezetting", "5. Tekst in Bezetting"))
l_sorts = (("artiest", "Uitvoerende"),
           ("locatie", "Locatie/datum", "dflt"),
           ("geen", "Niets"))


def get_infodict_for_index():
    return {"actlist": my.Act.objects.all().order_by('last_name'),
            "s_keuzes": s_keuzes,
            "s_sorts": s_sorts,
            "l_keuzes": l_keuzes,
            "l_sorts": l_sorts}


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
        selected = my.Act.objects.get(id=sel_id).get_name()
        kop += f" - selectie: artiest '{selected}'"
        selitem = sel_id
    elif keuze == s_keuzes[2][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += f" - selectie: titel bevat '{zoektxt}'"
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[3][0]:
        sel = sel.filter(produced_by__icontains=zoektxt)
        kop += f" - selectie: produced_by bevat '{zoektxt}'"
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[4][0]:
        sel = sel.filter(credits__icontains=zoektxt)
        kop += f" - selectie: credits bevat '{zoektxt}'"
        selitem = zoektxt
        altsel = ''
    elif keuze == s_keuzes[5][0]:
        sel = sel.filter(bezetting__icontains=zoektxt)
        kop += f" - selectie: bezetting bevat '{zoektxt}'"
        selitem = zoektxt
    else:
        meld = 'Gekozen selectie kon niet worden uitgevoerd'
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
            kop += ' - niet gesorteerd'
        else:
            meld = 'Gekozen selectie kon niet worden gesorteerd'
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
        selected = format(my.Act.objects.get(id=sel_id).get_name())
        kop += f" - selectie: artiest '{selected}'"
        selitem = sel_id
    elif keuze == l_keuzes[2][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += f" - selectie: titel bevat locatie '{zoektxt}'"
        selitem = zoektxt
        altsel = ''
    elif keuze == l_keuzes[3][0]:
        sel = sel.filter(name__icontains=zoektxt)
        kop += f" - selectie: titel bevat datum '{zoektxt}'"
        selitem = zoektxt
        altsel = ''
    elif keuze == l_keuzes[4][0]:
        sel = sel.filter(bezetting__icontains=zoektxt)
        kop += f" - selectie: bezetting bevat '{zoektxt}'"
        selitem = zoektxt
    else:
        meld = 'Gekozen selectie kon niet worden uitgevoerd'
    if not meld:
        if sortorder == l_sorts[0][0]:
            sel = sel.order_by('artist')
            kop += " - gesorteerd op artiest"
        elif sortorder == l_sorts[1][0]:
            sel = sel.order_by('name')
            kop += " gesorteerd op locatie/datum"
            altsort = s_sorts[2][0]
        elif sortorder == l_sorts[2][0]:
            kop += ' - niet gesorteerd'
        else:
            meld = 'Gekozen selectie kon niet worden gesorteerd'
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


def get_infodict_for_detail(soort, keuze, selitem, sortorder, item, type, actie):
    "ophalen variabalen voor scherm"
    album = my.Album.objects.get(pk=item)
    act_id = album.artist.id
    act_list = my.Album.objects.filter(artist=act_id)
    infodict = {"track_list": album.tracks.all().order_by('volgnr'),
                "opn_list": album.opnames.all(),
                "album": album,
                "soort": soort,
                "keuze": keuze,
                "selitem": selitem,
                "sortorder": sortorder,
                "o_soort": my.o_soort,
                "o_oms": my.o_oms,
                "act_id": act_id,
                "type": type,
                "actie": actie,
                "actlist": my.Act.objects.all().order_by('last_name')}
    if soort == 'album':
        infodict["kop"] = "Gegevens van album " + str(album)
        infodict["act_list"] = act_list.exclude(label="")
    elif soort == 'live':
        infodict["kop"] = "Gegevens van concert: " + str(album)
        infodict["act_list"] = act_list.filter(label="")
    else:
        infodict["meld"] = 'Albumtype kon niet bepaald worden'
    return infodict


def get_infodict_for_artists(filter):
    "ophalen variabelen voor scherm"
    return {"artiesten":
            my.Act.objects.all().filter(last_name__contains=f'{filter}').order_by('last_name'),
            "filter": filter}


def get_infodict_for_new_item(soort, item, type, artiest, keuze, selitem, sortorder):
    "ophalen variabelen voor scherm"
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
        else:
            data["o_soort"] = my.o_soort
    else:
        data["actie"] = "edit"
        if keuze == 'artiest':
            artiest = selitem
        elif keuze:
            data[keuze] = selitem
        data["act_id"] = int(artiest) if artiest else 0
        # eigenlijk moet hier voorzien gaan worden in andere mogelijkheden
        data["actlist"] = my.Act.objects.all().order_by('last_name')
    return data


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
        data.first_name = postdict[f'tNaam{item}']
        data.last_name = postdict[f'tSort{item}']
        data.save()
    else:
        all_artists = my.Act.objects.all().order_by('id')
        maxnum = int(all_artists.reverse()[0].id)
        all_keys = [x for x in postdict if x.startswith('tNaam') and len(x) > len('tNaam')]
        for key in all_keys:
            act = my.Act.objects.get(pk=int(key[5:]))
            first_name_entered = postdict[key]
            last_name_entered = postdict[f'tSort{key[5:]}']
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
            newact = my.Act.objects.create(id=maxnum, last_name=value, first_name=f_names[ix])
        filter = postdict['filter']
        if filter:
            nextpage += filter + '/'
    return nextpage


def do_track_update(postdict, item, subitem):
    "daadwerkelijk uitvoeren van de update; geeft referentie naar het album terug"
    album = my.Album.objects.get(id=item)
    new_track = False
    if subitem == 'all':
        tracks = list(album.tracks.all().order_by('volgnr'))
        tracks.reverse()
        maxnum = int(tracks[0].volgnr) if tracks else 0
        # maxnum = int(tracks[-1].volgnr) if tracks else 0
        names = postdict.getlist('txtTrack0')
        authors = postdict.getlist('txtBy0')
        texts = postdict.getlist('txtCred0')
        for ix, value in enumerate(names):
            maxnum += 1
            newtrack = my.Song.objects.create(volgnr=maxnum, name=value, written_by=authors[ix],
                                              credits=texts[ix])
            # newtrack.save()
            album.tracks.add(newtrack)
    elif subitem:
        tracks = [my.Song.objects.get(id=subitem)]
    else:
        new_track = True
        tracks = [my.Song.objects.create(volgnr=postdict['tNr'])]
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
            # newopn.save()
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
