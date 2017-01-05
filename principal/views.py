#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from principal.forms import SearchForm, UserForm
from principal.models import Artista, Album, Cancion, Profile

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
    
def canciones(request, genero=None):  
    page = request.GET.get('page', 1)
    
    if genero != None:
        canciones = Cancion.objects.filter(Generos__contains=genero)
        paginator = Paginator(canciones, 4)
    
    if genero == None:
        generos = todosLosGeneros("cancion")
        paginator = Paginator(generos, 12)
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('canciones.html',{'data':data, 'genero':genero},context_instance=RequestContext(request))

def albumes(request, genero=None):  
    page = request.GET.get('page', 1)
    
    if genero != None:
        albumes = Album.objects.filter(Generos__contains=genero)
        paginator = Paginator(albumes, 4)
    
    if genero == None:
        generos = todosLosGeneros("album")
        paginator = Paginator(generos, 12)
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('albumes.html',{'data':data, 'genero':genero},context_instance=RequestContext(request))

def artistas(request, genero=None):  
    page = request.GET.get('page', 1)
    
    if genero != None:
        artistas = Artista.objects.filter(Generos__contains=genero)
        paginator = Paginator(artistas, 4)
    
    if genero == None:
        generos = todosLosGeneros("artista")
        paginator = Paginator(generos, 12)
  
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    return render_to_response('artistas.html',{'data':data, 'genero':genero},context_instance=RequestContext(request))


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

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')

