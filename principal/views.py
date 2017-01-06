#encoding:utf-8
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from principal.forms import SearchForm, UserForm, PlaylistForm
from principal.models import Profile, Playlist
from utils import *


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
    else:
        form = SearchForm()
    
    return render_to_response('index.html',{"form":form,"numArtists":numArtists,"numAlbums":numAlbums,"numSongs":numSongs},context_instance=RequestContext(request))
    
def songs(request, genre=None, playlist=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        songs = Cancion.objects.filter(Generos__contains=genre)
        paginator = Paginator(songs, 4)
        
    if playlist != None:
        playlist = Playlist.objects.get(Nombre=playlist)
        songs = playlist.Canciones.all()
        paginator = Paginator(songs, 4)
    
    if genre == None and playlist == None:
        genres = allGenres("song")
        paginator = Paginator(genres, 12)
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('songs.html',{'data':data, 'genre':genre, 'playlist':playlist},context_instance=RequestContext(request))

def albums(request, genre=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        albums = Album.objects.filter(Generos__contains=genre)
        paginator = Paginator(albums, 4)
    else:
        genres = allGenres("album")
        paginator = Paginator(genres, 12)
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('albums.html',{'data':data, 'genre':genre},context_instance=RequestContext(request))

def artists(request, genre=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        artists = Artista.objects.filter(Generos__contains=genre)
        paginator = Paginator(artists, 4)
    else:
        genres = allGenres("artist")
        paginator = Paginator(genres, 12)
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('artists.html',{'data':data, 'genre':genre},context_instance=RequestContext(request))

def index(request):
    return searchForm(request)

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
    
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
    
    return render_to_response('artist.html',{'form':form,'artist':artist,'albums':albums},context_instance=RequestContext(request))

def newUser(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                repeatPass = form.cleaned_data['repeatPassword']
                firstName = form.cleaned_data['firstName']
                lastName = form.cleaned_data['lastName']
                email = form.cleaned_data['email']
                gender = form.cleaned_data['gender']
                
                user = User.objects.filter(username=username)
                if len(user) == 0:
                    if password == repeatPass:
                        user = User.objects.create_user(username=username, password=password)
                        user.first_name = firstName
                        user.last_name = lastName
                        user.email = email
                        user.save()
                        Profile.objects.create(user=user, gender=gender)
                
                        access = authenticate(username=username, password=password)
                        if access is not None:
                            if access.is_active:
                                login(request, access)
                                return HttpResponseRedirect('/userindex')
                            else:
                                return render_to_response('noactive.html', context_instance=RequestContext(request))
                    else:
                        messages.error(request, "Error: Both passwords must match.")
                else:
                    messages.error(request, "Error: Username currently in use.") 
        else:
            form = UserForm()
    else:
        return HttpResponseRedirect('/userindex')
    
    return render_to_response('newuser.html', {'userForm':form}, context_instance=RequestContext(request))

def loginUser(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            user = request.POST['username']
            passw = request.POST['password']
            access = authenticate(username=user, password=passw)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return HttpResponseRedirect('/userindex')
                else:
                    return render_to_response('noactive.html', context_instance=RequestContext(request))
            else:
                messages.error(request, "Access Error: User and password do not match or do not exist.")
        else:
            form = AuthenticationForm()
    else:
        return HttpResponseRedirect('/userindex')
    
    return render_to_response('login.html', {'userForm':form}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def userIndex(request):
    user = request.user
    return render_to_response('userindex.html', {'user':user}, context_instance=RequestContext(request))

def logoutUser(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def newPlaylist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            songs = form.cleaned_data['songs']
            profile = request.user.get_profile()
            
            playlist = Playlist.objects.get(Nombre=name)
            if playlist == None:
                playlist = Playlist.objects.create(Nombre=name,Profile=profile)
            
                for song in songs:
                    playlist.Canciones.add(Cancion.objects.get(Nombre=song))
            
                playlist.save()
                return HttpResponseRedirect('/playlists')
            else:
                messages.error(request, "Error: You don't have two playlists with the same name.")
    else:
        form = PlaylistForm()
    return render_to_response('playlistform.html', {'playlistForm':form}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def playlists(request, playlist=None):  
    page = request.GET.get('page', 1)
    
    if playlist != None:
        return HttpResponseRedirect('/songs/playlist/'+playlist)
    else:
        playlists = Playlist.objects.filter(Profile=request.user.get_profile())
        paginator = Paginator(playlists, 6)
        
    user = request.user
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('playlists.html',{'data':data, 'user':user},context_instance=RequestContext(request))