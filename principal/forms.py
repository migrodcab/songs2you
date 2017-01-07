#encoding:utf-8
from django import forms
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from principal.models import Playlist, Cancion

class SearchForm(forms.Form):
    criteria = forms.CharField(label="Search artists, albums or songs")
    
class UserForm(forms.Form):
    fields = (('Male','Male'),('Female','Female'))    
    
    username = forms.CharField(max_length=20, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput, label="Repeat Password, please")
    firstName = forms.CharField(max_length=100, label="First name")
    lastName = forms.CharField(max_length=100, label="Last name")
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(fields, label="Gender")
    
class PlaylistForm(forms.Form):
    fields = []
    for cancion in Cancion.objects.all():
        fields.append((cancion, cancion.Nombre))
    fields = tuple(fields)
    
    name = forms.CharField(max_length=100, label="Name")
    songs = forms.MultipleChoiceField(choices=fields, label="Songs")
            
def Make_AddSongToPlaylistForm(userId=None,post=None):
    fields = []
    if userId != None:
        profile = User.objects.get(id=userId).get_profile()
        for playlist in profile.playlist_set.all():
            fields.append((playlist, playlist.Nombre))
        fields = tuple(fields)
    
    class AddSongToPlaylistForm(forms.Form):
            playlists = forms.MultipleChoiceField(choices=fields, label="Playlists")
    
    if post != None:
        return AddSongToPlaylistForm(post)
    
    if userId != None:
        return AddSongToPlaylistForm()