"""unittests for ./albums/muziek/views.py
"""
import os
import types
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albums.settings')
django.setup()
from albums.muziek import views
# import albums.muziek.models as my  - datamanipulatie naar helpers verplaatst


def test_index(monkeypatch, capsys):
    """unittest for views.index
    """
    def mock_get_infodict():
        """stub
        """
        print('called util.get_infodict_for_index()')
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_index', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.index('request') == ('request', 'muziek/start.html', 'infodict')
    assert capsys.readouterr().out == 'called util.get_infodict_for_index()\n'


def test_select(monkeypatch, capsys):
    """unittest for views.select
    """
    def mock_get_infodict_a(*args):
        """stub
        """
        print('called util.get_infodict_for_album() with args', args)
        return 'infodict'
    def mock_get_infodict_c(*args):
        """stub
        """
        print('called util.get_infodict_for_concert() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_album', mock_get_infodict_a)
    monkeypatch.setattr(views.util, 'get_infodict_for_concert', mock_get_infodict_c)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    request = types.SimpleNamespace(GET={'soort': 'album'})
    assert views.select(request, 'album', 'x', 'y', 'z') == (
            request, 'muziek/select.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_album()"
                                       " with args ({'soort': 'album'}, 'x', 'album', 'z', 'y')\n")
    request = types.SimpleNamespace(GET={'soort': 'live'})
    assert views.select(request, 'live', 'x', 'y', 'z') == (
            request, 'muziek/select.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_concert()"
                                       " with args ({'soort': 'live'}, 'x', 'live', 'z', 'y')\n")
    request = types.SimpleNamespace(GET={})
    assert views.select(request) == (request, 'muziek/select.html',
                                    {'meld': 'Albumtype kon niet bepaald worden'})
    assert capsys.readouterr().out == ''


def test_sel_detail(monkeypatch):
    """unittest for views.sel_detail
    """
    request = types.SimpleNamespace(GET={'selAlbum': 'x', 'keuze': 'keuze', 'selitem': 'y',
                                         'sortorder': 'asc'})
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.sel_detail(request, 'soort', 'item') == '/muziek/soort/x/keuze/y/asc/'


def test_detail(monkeypatch, capsys):
    """unittest for views.detail
    """
    def mock_get_infodict(*args):
        """stub
        """
        print('called util.get_infodict_for_detail() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_detail', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.detail('request', 'x', 'y', 'z', 'a', 'b', 'c', 'd') == (
            'request', 'muziek/detail.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_detail() with args"
                                       " ('x', 'y', 'z', 'a', 'b', 'c', 'd')\n")


def test_edit(monkeypatch, capsys):
    """unittest for views.edit
    """
    def mock_detail(*args, **kwargs):
        """stub
        """
        print('called views.detail() with args', args, kwargs)
        return 'redirect'
    monkeypatch.setattr(views, 'detail', mock_detail)
    assert views.edit('request', 'x', 'y', 'z', 'a', 'b', 'c') == 'redirect'
    assert capsys.readouterr().out == ("called views.detail() with args ('request',"
                                       " 'x', 'y', 'z', 'a', 'b', 'c') {'actie': 'edit'}\n")


def test_edit_tracks(monkeypatch, capsys):
    """unittest for views.edit_tracks
    """
    def mock_detail(*args, **kwargs):
        """stub
        """
        print('called views.detail() with args', args, kwargs)
        return 'redirect'
    monkeypatch.setattr(views, 'detail', mock_detail)
    assert views.edit_tracks('request', 'x', 'y', 'z', 'a', 'b', 'c') == 'redirect'
    assert capsys.readouterr().out == ("called views.detail() with args ('request', 'x',"
                                       " 'y', 'z', 'a', 'b') {'type': 'track', 'actie': 'edit'}\n")


def test_edit_recs(monkeypatch, capsys):
    """unittest for views.edit_recs
    """
    def mock_detail(*args, **kwargs):
        """stub
        """
        print('called views.detail() with args', args, kwargs)
        return 'redirect'
    monkeypatch.setattr(views, 'detail', mock_detail)
    assert views.edit_recs('request', 'x', 'y', 'z', 'a', 'b', 'c') == 'redirect'
    assert capsys.readouterr().out == ("called views.detail() with args ('request', 'x',"
                                       " 'y', 'z', 'a', 'b') {'type': 'opname', 'actie': 'edit'}\n")


def test_list_artists(monkeypatch, capsys):
    """unittest for views.list_artists
    """
    def mock_get_infodict(*args):
        """stub
        """
        print('called util.get_infodict_for_artists() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_artists', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.list_artists('request', 'soort', 'actie', 'filter') == (
            'request', 'muziek/artiesten.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_artists() with args"
                                       " ('filter',)\n")


def test_new(monkeypatch, capsys):
    """unittest for views.new
    """
    def mock_get_infodict(*args):
        """stub
        """
        print('called util.get_infodict_for_new_item() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_new_item', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    # assert views.new('request', 'soort', 'item', 'track', 'y', 'z', 'a', 'b') == (
    #         'request', 'muziek/track.html', 'infodict')
    # assert capsys.readouterr().out == ("called util.get_infodict_for_new_item() with args"
    #                                    " ('soort', 'item', 'track', 'y', 'z')\n")
    # assert views.new('request', 'soort', 'item', 'opname', 'y', 'z', 'a', 'b') == (
    #         'request', 'muziek/opname.html', 'infodict')
    # assert capsys.readouterr().out == ("called util.get_infodict_for_new_item() with args"
    #                                    " ('soort', 'item', 'opname', 'y', 'z')\n")
    assert views.new('request', 'soort', 'item', 'x', 'y', 'z', 'a', 'b') == (
            'request', 'muziek/detail.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_new_item() with args"
                                       " ('soort', 'item', 'x', 'y', 'z', 'a', 'b')\n")


def test_new_track(monkeypatch, capsys):
    """unittest for views.new_track
    """
    # def mock_new(*args):
    #     print('called views.new() with args', args)
    #     return 'redirect'
    # monkeypatch.setattr(views, 'new', mock_new)
    # assert views.new_track('request', 'soort', 'item', 'x', 'y', 'z', 'a', 'b') == 'redirect'
    # assert capsys.readouterr().out == ("called views.new() with args ('request', 'soort', 'item',"
    #                                    " 'track', 'y', 'z', 'a', 'b')\n")
    def mock_get_infodict(*args):
        """stub
        """
        print('called util.get_infodict_for_new_item() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_new_item', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.new_track('request', 'soort', 'item', 'track', 'y', 'z', 'a', 'b') == (
            'request', 'muziek/track.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_new_item() with args"
                                       " ('soort', 'item', 'track', 'y', 'z', 'a', 'b')\n")


def test_new_rec(monkeypatch, capsys):
    """unittest for views.new_rec
    """
    # def mock_new(*args):
    #     print('called views.new() with args', args)
    #     return 'redirect'
    # monkeypatch.setattr(views, 'new', mock_new)
    # assert views.new_rec('request', 'soort', 'item', 'x', 'y', 'z', 'a', 'b') == 'redirect'
    # assert capsys.readouterr().out == ("called views.new() with args ('request', 'soort', 'item',"
    #                                    " 'opname', 'y', 'z', 'a', 'b')\n")
    def mock_get_infodict(*args):
        """stub
        """
        print('called util.get_infodict_for_new_item() with args', args)
        return 'infodict'
    monkeypatch.setattr(views.util, 'get_infodict_for_new_item', mock_get_infodict)
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.new_rec('request', 'soort', 'item', 'track', 'y', 'z', 'a', 'b') == (
            'request', 'muziek/opname.html', 'infodict')
    assert capsys.readouterr().out == ("called util.get_infodict_for_new_item() with args"
                                       " ('soort', 'item', 'opname', 'y', 'z', 'a', 'b')\n")


def test_new_artist(monkeypatch, capsys):
    """unittest for views.new_artist
    """
    monkeypatch.setattr(views, 'render', lambda *x: x)
    assert views.new_artist('request', 'soort') == ('request', 'muziek/artiest.html')


def test_update(monkeypatch, capsys):
    """unittest for views.update
    """
    def mock_artiest_update(*args):
        """stub
        """
        print('called util.do_artiest_update() with args', args)
        return 'redirect'
    def mock_track_update(*args):
        """stub
        """
        print('called util.do_track_update() with args', args)
        return types.SimpleNamespace(id='albumid')
    def mock_rec_update(*args):
        """stub
        """
        print('called util.do_rec_update() with args', args)
        return types.SimpleNamespace(id='albumid')
    def mock_album_update(*args):
        """stub
        """
        print('called util.do_album_update() with args', args)
        return types.SimpleNamespace(id='albumid')
    monkeypatch.setattr(views.util, 'do_artiest_update', mock_artiest_update)
    monkeypatch.setattr(views.util, 'do_track_update', mock_track_update)
    monkeypatch.setattr(views.util, 'do_rec_update', mock_rec_update)
    monkeypatch.setattr(views.util, 'do_album_update', mock_album_update)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    request = types.SimpleNamespace(POST={'keuze': 'k', 'selitem': 'i', 'sortorder': 'a'})
    assert views.update(request, 'artiest', 'x', 'y', 'z') == 'redirect'
    assert capsys.readouterr().out == ("called util.do_artiest_update() with args"
                                       f" ({request.POST}, 'x')\n")
    assert views.update(request, 'q', 'x', 'track', 'z') == '/muziek/q/albumid/k/i/a/'
    assert capsys.readouterr().out == ("called util.do_track_update() with args"
                                       f" ({request.POST}, 'x', 'z')\n")
    assert views.update(request, 'q', 'x', 'opname', 'z') == '/muziek/q/albumid/k/i/a/'
    assert capsys.readouterr().out == ("called util.do_rec_update() with args"
                                       f" ({request.POST}, 'x', 'z')\n")
    assert views.update(request, 'album', 'x', 'album', 'z') == '/muziek/album/albumid/k/i/a/'
    assert capsys.readouterr().out == ("called util.do_album_update() with args"
                                       f" ({request.POST}, 'album', 'x')\n")
    assert views.update(request, 'artiest', 'x', 'y', 'z', 'c', 's', 'd') == 'redirect'
    assert capsys.readouterr().out == ("called util.do_artiest_update() with args"
                                       f" ({request.POST}, 'x')\n")
    assert views.update(request, 'q', 'x', 'track', 'z', 'c', 's', 'd') == (
            '/muziek/q/albumid/c/s/d/')
    assert capsys.readouterr().out == ("called util.do_track_update() with args"
                                       f" ({request.POST}, 'x', 'z')\n")
    assert views.update(request, 'q', 'x', 'opname', 'z', 'c', 's', 'd') == (
            '/muziek/q/albumid/c/s/d/')
    assert capsys.readouterr().out == ("called util.do_rec_update() with args"
                                       f" ({request.POST}, 'x', 'z')\n")
    assert views.update(request, 'live', 'x', 'album', 'z', 'c', 's', 'd') == (
            '/muziek/live/albumid/c/s/d/')
    assert capsys.readouterr().out == ("called util.do_album_update() with args"
                                       f" ({request.POST}, 'live', 'x')\n")
    request = types.SimpleNamespace(POST={})
    assert views.update(request, 'album', 'x', 'album', 'z') == '/muziek/album/albumid/'
    assert capsys.readouterr().out == ("called util.do_album_update() with args"
                                       f" ({request.POST}, 'album', 'x')\n")


def test_update_tracks(monkeypatch, capsys):
    """unittest for views.update_tracks
    """
    def mock_update(*args):
        """stub
        """
        print('called views.update() with args', args)
        return 'redirect'
    monkeypatch.setattr(views, 'update', mock_update)
    assert views.update_tracks('request', 'srt', 'x', 'type', 'y', 'sel', 'z', 'a') == 'redirect'
    assert capsys.readouterr().out == ("called views.update() with args ('request', 'srt', 'x',"
                                       " 'track', 'all', 'sel', 'z', 'a')\n")


def test_update_single_track(monkeypatch, capsys):
    """unittest for views.update_single_track
    """
    def mock_update(*args):
        """stub
        """
        print('called views.update() with args', args)
        return 'redirect'
    monkeypatch.setattr(views, 'update', mock_update)
    assert views.update_single_track('request', 'srt', 'x', 'type', 'y', 'sel', 'z', 'a') == (
            'redirect')
    assert capsys.readouterr().out == ("called views.update() with args ('request', 'srt', 'x',"
                                       " 'track', 'y', 'sel', 'z', 'a')\n")


def test_update_recs(monkeypatch, capsys):
    """unittest for views.update_recs
    """
    def mock_update(*args):
        """stub
        """
        print('called views.update() with args', args)
        return 'redirect'
    monkeypatch.setattr(views, 'update', mock_update)
    assert views.update_recs('request', 'srt', 'x', 'type', 'y', 'sel', 'z', 'a') == 'redirect'
    assert capsys.readouterr().out == ("called views.update() with args ('request', 'srt', 'x',"
                                       " 'opname', 'all', 'sel', 'z', 'a')\n")


def test_update_single_rec(monkeypatch, capsys):
    """unittest for views.update_single_rec
    """
    def mock_update(*args):
        """stub
        """
        print('called views.update() with args', args)
        return 'redirect'
    monkeypatch.setattr(views, 'update', mock_update)
    assert views.update_single_rec('request', 'srt', 'x', 'type', 'y', 'sel', 'z', 'a') == (
            'redirect')
    assert capsys.readouterr().out == ("called views.update() with args ('request', 'srt', 'x',"
                                       " 'opname', 'y', 'sel', 'z', 'a')\n")


def test_update_artists(monkeypatch, capsys):
    """unittest for views.update_artists
    """
    def mock_update(*args):
        """stub
        """
        print('called views.update() with args', args)
        return 'redirect'
    monkeypatch.setattr(views, 'update', mock_update)
    assert views.update_artists('request', 'srt', 'x', 'type', 'y', 'sel', 'z', 'a') == 'redirect'
    assert capsys.readouterr().out == ("called views.update() with args ('request', 'srt', 'x',"
                                       " 'artist', 'all', 'sel', 'z', 'a')\n")
