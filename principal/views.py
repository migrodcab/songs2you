#encoding:utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.models import Artista, Album, Cancion


def index(request):
    numArtists = Artista.objects.count()
    numAlbums = Album.objects.count()
    numSongs = Cancion.objects.count()
    return render_to_response('index.html',{"numArtists":numArtists,"numAlbums":numAlbums,"numSongs":numSongs},context_instance=RequestContext(request))