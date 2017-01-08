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

from principal.forms import SearchForm, UserForm, PlaylistForm, Make_AddSongToPlaylistForm
from principal.models import Profile, Playlist
from utils import *


def searchForm(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    numArtists = Artista.objects.count()
    numAlbums = Album.objects.count()
    numSongs = Cancion.objects.count()
    
    form = SearchForm(request.POST)
    if form.is_valid():
        artists = Artista.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        albums = Album.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        songs = Cancion.objects.filter(Nombre__contains=form.cleaned_data['criteria'])
        return render_to_response('index.html',{'form':form,'artists':artists,'albums':albums,'songs':songs,'numArtists':numArtists,'numAlbums':numAlbums,'numSongs':numSongs, 'user':user},context_instance=RequestContext(request))
    else:
        form = SearchForm()
    
    return render_to_response('index.html',{"form":form,"numArtists":numArtists,"numAlbums":numAlbums,"numSongs":numSongs, "user":user},context_instance=RequestContext(request))
    
def songs(request, genre=None, playlist=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        songs = Cancion.objects.filter(Generos__contains=genre)
        paginator = Paginator(songs, 6)
        
    if playlist != None:
        playlist = Playlist.objects.get(Nombre=playlist)
        songs = playlist.Canciones.all()
        paginator = Paginator(songs, 6)
    
    if genre == None and playlist == None:
        genres = allGenres("song")
        paginator = Paginator(genres, 12)
    
    (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10) = pagination(paginator, page)
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('songs.html',{
                                            'data':data,
                                            'data1':data1,
                                            'data2':data2,
                                            'data3':data3,
                                            'data4':data4,
                                            'data5':data5,
                                            'data6':data6,
                                            'data7':data7,
                                            'data8':data8,
                                            'data9':data9,
                                            'data10':data10,
                                            'genre':genre,'playlist':playlist,'user':user
                                            },context_instance=RequestContext(request))

def albums(request, genre=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        albums = Album.objects.filter(Generos__contains=genre)
        paginator = Paginator(albums, 6)
    else:
        genres = allGenres("album")
        paginator = Paginator(genres, 12)
  
    (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10) = pagination(paginator, page)
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('albums.html',{
                                             'data':data,
                                             'data1':data1,
                                             'data2':data2,
                                             'data3':data3,
                                             'data4':data4,
                                             'data5':data5,
                                             'data6':data6,
                                             'data7':data7,
                                             'data8':data8,
                                             'data9':data9,
                                             'data10':data10,
                                             'genre':genre, 'user':user},context_instance=RequestContext(request))

def artists(request, genre=None):  
    page = request.GET.get('page', 1)
    
    if genre != None:
        artists = Artista.objects.filter(Generos__contains=genre)
        paginator = Paginator(artists, 6)
    else:
        genres = allGenres("artist")
        paginator = Paginator(genres, 12)
  
    (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10) = pagination(paginator, page)
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('artists.html',{
                                              'data':data,
                                              'data1':data1,
                                              'data2':data2,
                                              'data3':data3,
                                              'data4':data4,
                                              'data5':data5,
                                              'data6':data6,
                                              'data7':data7,
                                              'data8':data8,
                                              'data9':data9,
                                              'data10':data10,
                                              'genre':genre, 'user':user},context_instance=RequestContext(request))

def index(request):
    return searchForm(request)

def displayAlbum(request,albumId):
    album = get_object_or_404(Album, pk=albumId)
    songs = Cancion.objects.filter(Album=album)
    
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('album.html',{'form':form,'album':album,'songs':songs, 'user':user},context_instance=RequestContext(request))

def displayArtist(request,artistId):
    artist = get_object_or_404(Artista, pk=artistId)
    albums = Album.objects.filter(Artista=artist)
    
    if request.method=='POST':
        return searchForm(request)
    else:
        form = SearchForm()
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('artist.html',{'form':form,'artist':artist,'albums':albums, 'user':user},context_instance=RequestContext(request))

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
    
    return render_to_response('newuser.html', {'userForm':form, 'user':None}, context_instance=RequestContext(request))

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
    
    return render_to_response('login.html', {'userForm':form, 'user':None}, context_instance=RequestContext(request))

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
            
            playlists = Playlist.objects.filter(Nombre=name)
            if len(playlists) == 0:
                playlist = Playlist.objects.create(Nombre=name,Profile=profile)
            
                for song in songs:
                    playlist.Canciones.add(Cancion.objects.get(Nombre=song))
            
                playlist.save()
                return HttpResponseRedirect('/playlist')
            else:
                messages.error(request, "Error: You don't have two playlists with the same name.")
    else:
        form = PlaylistForm()
        
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    return render_to_response('playlistform.html', {'playlistForm':form, 'user':user}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def playlists(request, playlist=None, userId=None):  
    page = request.GET.get('page', 1)
    
    if playlist != None:
        return HttpResponseRedirect('/songs/playlist/'+playlist)
    elif userId != None:
        userView = Profile.objects.get(id=userId)
        playlists = Playlist.objects.filter(Profile=userView)
        paginator = Paginator(playlists, 9)
    else:
        userView = request.user.get_profile
        playlists = Playlist.objects.filter(Profile=userView)
        paginator = Paginator(playlists, 9)
        
    user = request.user
  
    (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10) = pagination(paginator, page)
    
    return render_to_response('playlists.html',{
                                                'data':data,
                                                'data1':data1,
                                                'data2':data2,
                                                'data3':data3,
                                                'data4':data4,
                                                'data5':data5,
                                                'data6':data6,
                                                'data7':data7,
                                                'data8':data8,
                                                'data9':data9,
                                                'data10':data10,
                                                'user':user, 'userView':userView},context_instance=RequestContext(request))

@login_required(login_url='/login')
def addSongToPlaylist(request, songId):
    user = request.user
    id = user.id
    if request.method == 'POST':
        form = Make_AddSongToPlaylistForm(userId=id, post=request.POST)
        if form.is_valid():
            playlists = form.cleaned_data['playlists']
            song = Cancion.objects.get(id=str(songId))
            for list in playlists:
                playlist = Playlist.objects.get(Nombre=list)
                playlist.Canciones.add(song)
                playlist.save()
            return HttpResponseRedirect('/playlist')
    else:
        form = Make_AddSongToPlaylistForm(userId=id)
    
    return render_to_response('addsongtoplaylistform.html', {'playlistForm':form, 'songId':songId, 'user':user}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def users(request): 
    user = request.user 
    page = request.GET.get('page', 1)
    
    users = Profile.objects.exclude(user=request.user)
    
    paginator = Paginator(users, 12)
  
    (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10) = pagination(paginator, page)
    
    return render_to_response('users.html',{
                                            'data':data,
                                            'data1':data1,
                                            'data2':data2,
                                            'data3':data3,
                                            'data4':data4,
                                            'data5':data5,
                                            'data6':data6,
                                            'data7':data7,
                                            'data8':data8,
                                            'data9':data9,
                                            'data10':data10,
                                            'user':user},context_instance=RequestContext(request))