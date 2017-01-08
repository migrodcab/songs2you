# encoding:utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import IntegerField


class Artista(models.Model):
    # (id,name,members,genre,styles,photo)
    id = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Miembros = models.CharField(max_length=140)
    Generos = models.CharField(max_length=140)
    Estilos = models.CharField(max_length=140)
    Imagen = models.URLField()
    
    def __unicode__(self):
        return self.Nombre
    
class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Etiqueta = models.CharField(max_length=30)
    Generos = models.CharField(max_length=140)
    Estilos = models.CharField(max_length=140)
    FechaPublicacion = models.DateField(null=True,default=None)
    ImagenPortada = models.URLField()
    Duracion = models.TimeField(null=True,default=None)
    Artista = models.ForeignKey(Artista)
    
    def __unicode__(self):
        return self.Nombre + " (" + str(self.FechaPublicacion) + ")"
    
class Cancion(models.Model):
    # (id,track_number,name,duration,genre,styles,video_id)
    id = models.IntegerField(primary_key=True)
    NumeroCancion = IntegerField()
    Nombre = models.CharField(max_length=50)
    EnlaceYouTube = models.URLField()
    Generos = models.CharField(max_length=140)
    Estilos = models.CharField(max_length=140)
    Duracion = models.TimeField(null=True,default=None)
    Album = models.ForeignKey(Album)
    
    def __unicode__(self):
        return self.Nombre
    
class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    gender = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
    
class Playlist(models.Model):
    Nombre = models.CharField(max_length=50)
    Profile = models.ForeignKey(Profile)
    Canciones = models.ManyToManyField(Cancion)
    
    def __unicode__(self):
        return self.Nombre
    
    