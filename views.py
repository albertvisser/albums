# todo:
# - kruimelpad
# - opnames
# - acts - bezettingen - artiesten gedeelte

## from django.template import Context, loader
## from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
import pythoneer.muziek.models as my
from django.shortcuts import render_to_response, get_object_or_404
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
    )
o_oms = (
    'eigen box',
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
    postdict = request.POST
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
        if keuze == s_keuzes[0][0]:
            kop += " - selectie: alles"
            selitem = "alles"
        elif keuze == s_keuzes[1][0]:
            sel = sel.filter(artist=sel_id)
            kop += " - selectie: artiest '%s'" % my.Act.objects.get(id=sel_id)
            selitem = sel_id
        elif keuze == s_keuzes[2][0]:
            sel = sel.filter(name__icontains=zoektxt)
            kop += " - selectie: titel bevat '%s'" % zoektxt
            selitem = zoektxt
        elif keuze == s_keuzes[3][0]:
            sel = sel.filter(produced_by__icontains=zoektxt)
            kop += " - selectie: produced_by bevat '%s'" % zoektxt
            selitem = zoektxt
        elif keuze == s_keuzes[4][0]:
            sel = sel.filter(credits__icontains=zoektxt)
            kop += " - selectie: credits bevat '%s'" % zoektxt
            selitem = zoektxt
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
            elif sortorder == s_sorts[2][0]:
                sel = sel.order_by('release_year')
                kop += " gesorteerd op jaar"
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
        if keuze == l_keuzes[0][0]:
            kop += " - selectie: alles"
            selitem = "alles"
        elif keuze == l_keuzes[1][0]:
            sel = sel.filter(artist=sel_id)
            kop += " - selectie: artiest '%s'" % my.Act.objects.get(id=sel_id)
            selitem = sel_id
        elif keuze == l_keuzes[2][0]:
            sel = sel.filter(name__icontains=zoektxt)
            kop += " - selectie: titel bevat locatie '%s'" % zoektxt
            selitem = zoektxt
        elif keuze == l_keuzes[3][0]:
            sel = sel.filter(produced_by__icontains=zoektxt)
            kop += " - selectie: titel bevat datum '%s'" % zoektxt
            selitem = zoektxt
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
            if len(sel) == 0:
                meld = "Geen concerten gevonden"
            else:
                meld = "Kies een concertopname uit de lijst:"
                info_dict["sel"] = sel
        info_dict["meld"] = meld
    else:
        info_dict["meld"] = 'Albumtype kon niet bepaald worden'
    # toon een lijst met my.Album items
    return render_to_response('muziek/select.html',info_dict)

def sel_detail(request, soort="", item=""):
    postdict = request.POST
    return HttpResponseRedirect("/muziek/%s/%s/%s/%s/%s/" % (soort, postdict["selAlbum"],
        postdict['keuze'], postdict['selitem'], postdict['sortorder']))

def detail(request, soort="", keuze="", selitem="", sortorder="", item=""):
    info_dict = {}
    ## getdict = request.GET
    ## getpath = request.get_full_path()
    ## return HttpResponse(">>{} {}<<".format(str(getdict), getpath))
    bingo = my.Album.objects.get(pk=item)
    act_id = bingo.artist.id
    ## if bingo.bezetting:
        ## info_dict["bezet"] = "; ".join([str(x) for x in bingo.bezetting.artists.all()])
    act_list = my.Album.objects.filter(artist=act_id)
    info_dict["track_list"] = bingo.tracks.all().order_by('volgnr')
    info_dict["opn_list"] = bingo.opnames.all()
    info_dict["album"] = bingo
    info_dict["soort"] = soort
    info_dict["keuze"] = keuze
    info_dict["selitem"] = selitem
    info_dict["sortorder"] = sortorder
    info_dict["o_soort"] = o_soort
    info_dict["o_oms"] = o_oms
    info_dict["act_id"] = act_id
    info_dict["actlist"] = my.Act.objects.all().order_by('last_name')
    if soort == 'album':
        info_dict["kop"] = "Gegevens van album " + str(bingo)
        info_dict["act_list"] = act_list.exclude(label="")
    elif soort == 'live':
        info_dict["kop"] = "Gegevens van concert: " + str(bingo)
        info_dict["act_list"] = act_list.filter(label="")
    else:
        info_dict["meld"] = 'Albumtype kon niet bepaald worden'
    return render_to_response('muziek/detail.html',info_dict)

def artiest(request, actie=""):
    # toon een lijst met my.Act items
    return render_to_response('muziek/artiesten.html',{
        "artiesten": my.Act.objects.all().order_by('last_name'),
        })

def nieuw(request, soort="", item="", type=""):
    if soort in ("album", "live"):
        if type == "track":
            album = my.Album.objects.get(id=item)
            aantal = album.tracks.count()
            return render_to_response("muziek/track.html",{
                "kop": type.join(("nieuw(e) "," opvoeren")),
                "soort": soort,
                "album": album,
                "nieuw": True,
                "volgnr": str(aantal + 1)
                })
        elif type == "opname":
            album = my.Album.objects.get(id=item)
            return render_to_response("muziek/opname.html",{
                "kop": type.join(("nieuw(e) "," opvoeren")),
                "album": album,
                "nieuw": True,
                "soort": soort,
                "o_soort": o_soort,
                })
        return render_to_response('muziek/detail.html',{
            "kop": soort.join(("nieuw(e) "," opvoeren")),
            "soort": soort,
            "nieuw": True,
            "actlist": my.Act.objects.all().order_by('last_name'),
            })
    elif soort == "artiest":
        return render_to_response('muziek/artiest.html',{
            "kop": soort.join(("nieuwe "," opvoeren")),
            "soort": soort,
            "artiesten": "lijst",
            "artiest": "nieuw"
            })

def wijzig(request, soort="", item="", type="", subitem="", actie=""):
    postdict = request.POST
    return HttpResponse('>{}<'.format(postdict))
    if type == "track":
        album = my.Album.objects.get(id=item)
        if subitem:
            track = my.Song.objects.get(id=subitem)
            if actie == "edit":
                return render_to_response("muziek/track.html",{
                    "kop": type + " wijzigen",
                    "soort": soort,
                    "album": album,
                    "track": track,
                    })
        else:
            track = my.Song()
        wijzig = False
        if int(postdict["tNr"]) != track.volgnr:
            track.volgnr = int(postdict["tNr"])
            wijzig = True
        if postdict["tNaam"] != track.name:
            track.name = postdict["tNaam"]
            wijzig = True
        if postdict["tDoor"] != track.written_by:
            track.written_by = postdict["tDoor"]
            wijzig = True
        if postdict["tCredits"] != track.credits:
            track.credits = postdict["tCredits"]
            wijzig = True
        if wijzig:
            track.save()
            if not subitem:
                album.tracks.add(track)
        return HttpResponseRedirect("/muziek/%s/%s/" % (soort,item))
    elif type == "opname":
        album = my.Album.objects.get(id=item)
        if subitem:
            opname = my.Opname.objects.get(id=subitem)
            if actie == "edit":
                return render_to_response("muziek/opname.html",{
                    "kop": type + " wijzigen",
                    "soort": soort,
                    "album": album,
                    "opname": opname,
                    "o_soort": o_soort,
                    })
        else:
            opname = my.Opname()
        wijzig = False
        if postdict["selMed"] != opname.type:
            opname.type = postdict["selMed"]
            wijzig = True
        if postdict["tOms"] != opname.oms:
            opname.oms = postdict["tOms"]
            wijzig = True
        if wijzig:
            opname.save()
            if not subitem:
                album.opnames.add(opname)
        return HttpResponseRedirect("/muziek/%s/%s/" % (soort,item))
    if soort in ("album", "live"):
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
            postdict['keuze'], postdict['selitem'], postdict['sortorder']))
    elif soort == "artiest":
        if keuze == "add":
            # na toevoegen aan de database: bepaal new_id
            return HttpResponseRedirect("/muziek/artiest/lijst/")
        return render_to_response('muziek/artiest.html',{
            "artiesten": "lijst",
            "artiest": "nieuw"
            })

# kies bezetting: eigenlijk moet de gebruiker alleen uit de bezettingen bij de Act kunnen kiezen
# terwijl bij raadplegen deze (nog) niet in een select getoond wordt
# edit song: er een toevoegen (of weghalen) zou je vanuit het totaalscherm moeten kunnen,
#   door de titel te wijzigen, voor details moet je naar een apart schermpje kunnen
#   dat kan alleen/het beste door niet eenzelfde opanem aan meer albums te koppelen
# edit opname: de gebruiker kan
# - een type kiezen
# - een locatie kiezen of een omschrijvinkje invullen
