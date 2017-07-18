"""Page definitions on project level
"""
from django.shortcuts import render_to_response
from albums.settings import MEDIA_ROOT


def index(request):
    "show start page"
    return render_to_response('index.html', {})


def viewdoc(request):
    "view an uploaded document"
    parts = request.path.split('files/')
    return render_to_response(MEDIA_ROOT + parts[1], {})
