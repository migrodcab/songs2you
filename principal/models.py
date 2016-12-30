# encoding:utf-8
from django.db import models


class Artista(models.Model):
    Nombre = models.CharField(max_length=50)
    Miembros = models.CharField(max_length=140)
    Generos = models.CharField(max_length=140)
    
    def __unicode__(self):
        return self.Nombre
    
class Album(models.Model):
    Nombre = models.CharField(max_length=50)
    FechaPublicacion = models.DateField()
    Generos = models.CharField(max_length=140)
    ImagenPortada = models.URLField()
    Artista = models.ForeignKey(Artista)
    
    def __unicode__(self):
        return self.Nombre + " (" + str(self.FechaPublicacion) + ")"
    
class Cancion(models.Model):
    Nombre = models.CharField(max_length=50)
    EnlaceYouTube = models.URLField()
    Generos = models.CharField(max_length=140)
    Album = models.ForeignKey(Album)
    
    def __unicode__(self):
        return self.Nombre