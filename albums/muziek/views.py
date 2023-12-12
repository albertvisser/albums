"""Code to build pages to show
"""
from django.http import HttpResponseRedirect  # , Http404, HttpResponse
from django.shortcuts import render
# import albums.muziek.models as my
import albums.muziek.helpers as util


def index(request):
    """Prepare to show start page
    """
    return render(request, 'muziek/start.html', util.get_infodict_for_index())


def select(request, soort="", keuze="", sortorder="", selitem=""):
    """Prepare Selection Page
    """
    postdict = request.GET
    if soort == 'album':
        info_dict = util.get_infodict_for_album(postdict, keuze, soort, selitem, sortorder)
    elif soort == 'live':
        info_dict = util.get_infodict_for_concert(postdict, keuze, soort, selitem, sortorder)
    else:
        info_dict = {"meld": 'Albumtype kon niet bepaald worden'}
    return render(request, 'muziek/select.html', info_dict)


def sel_detail(request, soort="", item=""):
    "snel naar een ander album van dezelfde artiest"
    postdict = request.GET
    return HttpResponseRedirect(f"/muziek/{soort}/{postdict['selAlbum']}/{postdict['keuze']}/"
                                f"{postdict['selitem']}/{postdict['sortorder']}/")


def detail(request, soort="", keuze="", selitem="", sortorder="", item="", type="", actie=""):
    """Detailgegevens van een album
    """
    info_dict = util.get_infodict_for_detail(soort, keuze, selitem, sortorder, item, type, actie)
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
    return render(request, 'muziek/artiesten.html', util.get_infodict_for_artists(filter))


# nieuw -> new
def new(request, soort="", item="", type="", artiest="", keuze="", selitem="", sortorder=""):
    """opvoeren van een album of artiest
    """
    data = util.get_infodict_for_new_item(soort, item, type, artiest, keuze, selitem, sortorder)
    # if type == 'track':
    #     return render(request, "muziek/track.html", data)
    # elif type == 'opname':
    #     return render(request, "muziek/opname.html", data)
    return render(request, 'muziek/detail.html', data)


# nieuw voor track -> new_track
def new_track(request, soort="", item="", type="", artiest="", keuze="", selitem="", sortorder=""):
    "openzetten track details voor opvoeren nieuw track"
    # return new(request, soort, item, "track", artiest, keuze, selitem, sortorder)
    data = util.get_infodict_for_new_item(soort, item, "track", artiest, keuze, selitem, sortorder)
    return render(request, "muziek/track.html", data)


# nieuw voor opname -> new_rec
def new_rec(request, soort="", item="", type="", artiest="", keuze="", selitem="", sortorder=""):
    "openzetten opname details voor opvoeren nieuwe opname"
    # return new(request, soort, item, "opname", artiest, keuze, selitem, sortorder)
    data = util.get_infodict_for_new_item(soort, item, "opname", artiest, keuze, selitem, sortorder)
    return render(request, "muziek/opname.html", data)


def new_artist(request, soort=''):
    # data["artiesten"] = "lijst"
    # data["artiest"] = "nieuw"
    # artiest.html gebruikt geen variabelen
    # soort komt mee vanuit de urlconf
    return render(request, 'muziek/artiest.html')  # , data)


# wijzig -> update
def update(request, soort="", item="", type="", subitem="", keuze="", selitem="", sortorder=""):
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
        nextpage = util.do_artiest_update(postdict, item)
        return HttpResponseRedirect(nextpage)
    if type == "track":
        album = util.do_track_update(postdict, item, subitem)
    elif type == "opname":
        album = util.do_rec_update(postdict, item, subitem)
    elif soort in ("album", "live"):
        album = util.do_album_update(postdict, soort, item)
    if keuze:
        return HttpResponseRedirect(f"/muziek/{soort}/{album.id}/{keuze}/{selitem}/{sortorder}/")
    return HttpResponseRedirect(f"/muziek/{soort}/{album.id}/")


# update voor track/all -> update_tracks
def update_tracks(request, soort="", item="", type="", subitem="", keuze="", selitem="",
                  sortorder=""):
    "bijwerken alle tracks in database in één keer"
    # return update(request, soort=soort, item=item, type="track", subitem="all", keuze=keuze,
    #               selitem=selitem, sortorder=sortorder)
    return update(request, soort, item, "track", "all", keuze, selitem, sortorder)


# update voor track -> update_single_track
def update_single_track(request, soort="", item="", type="", subitem="", keuze="", selitem="",
                        sortorder=""):
    "bijwerken track in database"
    # return update(request, soort=soort, item=item, type="track", subitem=subitem, keuze=keuze,
    #               selitem=selitem, sortorder=sortorder)
    return update(request, soort, item, "track", subitem, keuze, selitem, sortorder)


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
