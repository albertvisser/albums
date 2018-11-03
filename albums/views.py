"""Page definitions on project level
"""
from django.shortcuts import render
from albums.settings import MEDIA_ROOT


def index(request):
    "show start page"
    return render(request, 'index.html', {})


def viewdoc(request):
    "view an uploaded document"
    parts = request.path.split('files/')
    return render(request, MEDIA_ROOT + parts[1], {})
