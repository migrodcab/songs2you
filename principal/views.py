#encoding:utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.forms import SearchForm
from principal.models import Artista, Album, Cancion


def index(request):
    numArtists = Artista.objects.count()
    numAlbums = Album.objects.count()
    numSongs = Cancion.objects.count()
    
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            artists = Artista.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
            albums = Album.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
            songs = Cancion.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
            return render_to_response('index.html',{'form':form,'artists':artists,'albums':albums,'songs':songs,'numArtists':numArtists,'numAlbums':numAlbums,'numSongs':numSongs},context_instance=RequestContext(request))
    else:
        form = SearchForm()
    
    return render_to_response('index.html',{"form":form,"numArtists":numArtists,"numAlbums":numAlbums,"numSongs":numSongs},context_instance=RequestContext(request))