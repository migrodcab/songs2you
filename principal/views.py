#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from principal.forms import SearchForm
from principal.models import Artista, Album, Cancion


def searchForm(request):
    numArtists = Artista.objects.count()
    numAlbums = Album.objects.count()
    numSongs = Cancion.objects.count()
    
    form = SearchForm(request.POST)
    if form.is_valid():
        artists = Artista.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        albums = Album.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        songs = Cancion.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        return render_to_response('index.html',{'form':form,'artists':artists,'albums':albums,'songs':songs,'numArtists':numArtists,'numAlbums':numAlbums,'numSongs':numSongs},context_instance=RequestContext(request))

def index(request):
    numArtists = Artista.objects.count()
    numAlbums = Album.objects.count()
    numSongs = Cancion.objects.count()
    
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
    
    return render_to_response('index.html',{"form":form,"numArtists":numArtists,"numAlbums":numAlbums,"numSongs":numSongs},context_instance=RequestContext(request))

def canciones(request):
    canciones = Cancion.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(canciones, 4)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    #return render(request, 'canciones.html', { 'data': data })
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
    
    return render_to_response('canciones.html',{'form':form,'data':data},context_instance=RequestContext(request))

def displayAlbum(request,albumId):
    album = get_object_or_404(Album, pk=albumId)
    songs = Cancion.objects.filter(Album=album)
    
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
    
    return render_to_response('album.html',{'form':form,'album':album,'songs':songs},context_instance=RequestContext(request))

def displayArtist(request,artistId):
    artist = get_object_or_404(Artista, pk=artistId)
    albums = Album.objects.filter(Artista=artist)
    
    return render_to_response('artist.html',{'artist':artist,'albums':albums},context_instance=RequestContext(request))