# todo:
# - kruimelpad
# - opnames
# - acts - bezettingen - artiesten gedeelte

## from django.template import Context, loader
## from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
import albums.muziek.models as my
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

s_keuzes = (
    ("alles", "1. Niet zoeken, alles tonen"),
    ("artiest", "2. Uitvoerende: ","dflt"),
    ("titel", "3. Titel"),
    ## ("opname", "Opname") ,
    ("producer", "4. Producer"),
    ("credits", "5. Vermelding in Credits"),
    ("bezetting", "6. Vermelding in Bezetting"),
    )
s_sorts = (
    ("artiest", "Uitvoerende"),
    ("titel", "Titel"),
    ("jaar", "Jaar","dflt"),
    ## ("opname", "Opname" ),
    ("geen", "Niets"),
    )
l_keuzes = (
    ("alles", "1. Niet zoeken, alles tonen"),
    ("artiest", "2. Uitvoerende: ","dflt"),
    ## ("opname", "Opname" ),
    ("locatie", "3. Locatie"),
    ("datum", "4. Datum"),
    ("bezetting", "5. Vermelding in Bezetting"),
    )
l_sorts = (
    ("artiest", "Uitvoerende"),
    ## ("locatie", "Locatie"),
    ## ("datum", "Datum"),
    ("locatie", "Locatie/datum","dflt"),
    ## ("opname", "Opname" ),
    ("geen", "Niets"),
    )
o_soort = (
    'Cassette',
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
    )
o_oms = (
    'eigen doosje',
    'map A-E',
    'map F-S',
    'map T-Z',
    'map Live',
    )
def index(request):
    # bij "uitvoerende": presenteer een lijst met my.Act items (2x)
    return render_to_response('muziek/start.html',{
        "actlist": my.Act.objects.all().order_by('last_name'),
        "s_keuzes": s_keuzes,
        "s_sorts": s_sorts,
        "l_keuzes": l_keuzes,
        "l_sorts": l_sorts,
        })

def select(request, soort="", keuze="", sortorder="", selitem=""):
    info_dict = {}
    ## postdict = request.POST
    postdict = request.GET
    meld = ''
    if soort == 'album':
        if selitem:
            if keuze == s_keuzes[1][0]:
                sel_id = selitem
            else:
                zoektxt = selitem
        if 'selZoekS' in postdict:
            keuze = postdict['selZoekS']
        if 'selArtiest' in postdict:
            sel_id = postdict['selArtiest'] #  Act.id
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
            info_dict["actlist"] = my.Act.objects.all()
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
    elif soort == 'live':
        # uitgangspunt: bij een "concert" zit alle informatie (dwz locatie en datum) in de titel
        if selitem:
            if keuze == l_keuzes[1][0]:
                sel_id = selitem
            else:
                zoektxt = selitem
        if 'selZoekL' in postdict:
            keuze = postdict['selZoekL']
        if 'selArtiest' in postdict:
            sel_id = postdict['selArtiest'] #  Act.id
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
                ## sel = sel.order_by('release_year')
                ## kop += " gesorteerd op jaar"
            ## elif sortorder == s_sorts[3]:
                pass
            else:
                meld = 'Gekozen selectie kon niet gesorteerd worden'
        if not meld:
            info_dict["kop"] = kop
            info_dict["keuze"] = keuze
            info_dict["soort"] = soort
            info_dict["sortorder"] = sortorder
            info_dict["selitem"] = selitem
            info_dict["actlist"] = my.Act.objects.all()
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
    else:
        info_dict["meld"] = 'Albumtype kon niet bepaald worden'
    # toon een lijst met my.Album items
    return render_to_response('muziek/select.html', info_dict)

def sel_detail(request, soort="", item=""):
    postdict = request.GET
    return HttpResponseRedirect("/muziek/%s/%s/%s/%s/%s/" % (soort, postdict["selAlbum"],
        postdict['keuze'], postdict['selitem'], postdict['sortorder']))

def detail(request, soort="", keuze="", selitem="", sortorder="", item="", type="",
        actie=""):
    info_dict = {}
    ## getdict = request.GET
    ## getpath = request.get_full_path()
    ## return HttpResponse(">>{} {}<<".format(str(getdict), getpath))
    album = my.Album.objects.get(pk=item)
    act_id = album.artist.id
    ## if album_or_concert.bezetting:
        ## info_dict["bezet"] = "; ".join([str(x) for x in album_or_concert.bezetting.artists.all()])
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
    return render_to_response('muziek/detail.html',info_dict,
        context_instance=RequestContext(request))

def artiest(request, actie="", filter=""):
    # toon een lijst met my.Act items
    return render_to_response('muziek/artiesten.html', {
        "artiesten": my.Act.objects.all().filter(
            last_name__contains='{}'.format(filter)).order_by('last_name'),
        "filter": filter})

def nieuw(request, soort="", item="", type="", artiest="", keuze="",
        selitem="", sortorder=""):
    data = {
        "kop": soort.join(("nieuwe "," opname opvoeren")),
        "soort": soort,
        "keuze": keuze,
        "selitem": selitem,
        "sortorder": sortorder,
        }
    if soort in ("album", "live"):
        data["nieuw"] = True
        if type in ('track', 'opname'):
            data["kop"] = type.join(("nieuw(e) "," opvoeren"))
            album = my.Album.objects.get(id=item)
            aantal = album.tracks.count()
            data["album"] = album
            if type == "track":
                data["volgnr"] = str(aantal + 1)
                return render_to_response("muziek/track.html",data)
            else:
                data["o_soort"] = o_soort
                return render_to_response("muziek/opname.html", data)
        data["actie"] = "edit"
        if keuze == 'artiest':
            artiest = selitem
        elif keuze:
            data[keuze] = selitem
        data["act_id"] = int(artiest) if artiest else 0
        # eigenlijk moet hier voorzien gaan worden in andere mogelijkheden
        data["actlist"] = my.Act.objects.all().order_by('last_name')
        return render_to_response('muziek/detail.html', data)
    elif soort == "artiest":
        data["artiesten"] = "lijst"
        data["artiest"] = "nieuw"
        return render_to_response('muziek/artiest.html', data)

def wijzig(request, soort="", item="", type="", subitem="", actie="", keuze="",
        selitem="", sortorder=""):
    postdict = request.POST
    ## return HttpResponse('soort: {} item: {} type: {} subitem: {} actie: {}'. format(
        ## soort, item, type, subitem, actie))
    if not keuze and 'keuze' in postdict:
        keuze = postdict['keuze']
    if not selitem and 'selitem' in postdict:
        selitem = postdict['selitem']
    if not sortorder and 'sortorder' in postdict:
        sortorder = postdict['sortorder']
    if soort == "artiest":
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
                newact = my.Act.objects.create(id=maxnum, last_name=value,
                    first_name = f_names[ix])
                newact.save()
            filter = postdict['filter']
            if filter:
                nextpage += filter + '/'
        return HttpResponseRedirect(nextpage)

    elif type == "track":
        album = my.Album.objects.get(id=item)
        new_track = False
        if subitem == 'all':
            ## max = int(my.Songs.all().order_by('id').reverse()[0].id)
            tracks = album.tracks.all().order_by('volgnr')
            tracks = list(tracks)
            tracks.reverse()
            ## return HttpResponse('{}'.format(tracks))
            maxnum = int(tracks[0].volgnr) if tracks else 0
            names = postdict.getlist('txtTrack0')
            authors = postdict.getlist('txtBy0')
            texts = postdict.getlist('txtCred0')
            for ix, value in enumerate(names):
                maxnum += 1
                newtrack = my.Song.objects.create(volgnr=maxnum, name=value,
                    written_by=authors[ix], credits=texts[ix])
                newtrack.save()
                album.tracks.add(newtrack)
        elif subitem:
            tracks = [my.Song.objects.get(id=subitem)]
        else:
            new_track = True
            tracks = [my.Song.objects.create(id=postdict['tNr'])]
        ## return HttpResponse('{} {}'.format(tracks, new_track))
        for track in tracks:
            wijzig = False
            ## return HttpResponse('{} {}'.format(track.id, track.name))
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
                if new_track: # not subitem:
                    album.tracks.add(track)

    elif type == "opname":
        album = my.Album.objects.get(id=item)
        if subitem == 'all':
            opnames = list(album.opnames.all()) ##.order_by('volgnr')
            ## maxnum = int(opnames.reverse()[0].volgnr)
            types = postdict.getlist('selMed0')
            texts = postdict.getlist('txtOms0')
            for ix, value in enumerate(types):
                ## maxnum += 1
                newopn = my.Opname.objects.create(type=value, oms=texts[ix]) # volgnr=maxnum,
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

    elif soort in ("album", "live"):
        act = my.Act.objects.get(id=postdict["selArtiest"])
        if not item:
            olddict = {}
            album = my.Album.objects.create(artist=act,name=postdict["txtTitel"])
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
            if postdict["txtLabel"] != album.label:
                album.label = postdict["txtLabel"]
                wijzig = True
            if postdict["txtJaar"] != album.release_year:
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

    return HttpResponseRedirect("/muziek/%s/%s/%s/%s/%s/" % (soort, album.id,
        keuze, selitem, sortorder))

# kies bezetting: eigenlijk moet de gebruiker alleen uit de bezettingen bij de Act kunnen kiezen
# terwijl bij raadplegen deze (nog) niet in een select getoond wordt
# edit song: er een toevoegen (of weghalen) zou je vanuit het totaalscherm moeten kunnen,
#   door de titel te wijzigen, voor details moet je naar een apart schermpje kunnen
#   dat kan alleen/het beste door niet eenzelfde opanem aan meer albums te koppelen
# edit opname: de gebruiker kan
# - een type kiezen
# - een locatie kiezen of een omschrijvinkje invullen
