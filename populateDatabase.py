#encoding:iso-8859-15

'''
Created on 30/12/2016

@author: Javier Garcia (javgarcal@alum.us.es)
'''

import datetime, re

from principal.models import Artista, Album, Cancion

import codecs, sys, sqlite3, csv

from django.db.transaction import commit_on_success

from principal.models import *

reload(sys)
sys.setdefaultencoding('UTF8')  # @UndefinedVariable

def load(detailed):
    
    print "---------------------------------------------------------"
    print "                POPULATE DATABASE 1.0                    "
    print "---------------------------------------------------------"
    print ""
    
    @commit_on_success
    def loadArtists():
        
        print "[INFO] Loading artists..."
        
        num_lines = sum(1 for line in open('dataset/artists.csv')) #@UnusedVariable
        
        print "[INFO] Detected " + str(num_lines) + " items"
        
        with codecs.open('dataset/artists.csv', 'r', encoding='iso-8859-15') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # (id,name,members,genre,styles,photo)
            for row in reader:
                try:
                    Artista.objects.create(id=row[0],Nombre=row[1],Miembros=row[2],Generos=row[3],Estilos=row[4],Imagen=row[5])
                except:
                    if detailed:
                        print "[WARNING] The artist [" + ';'.join(row) + "] has not been considered."
                        
        print "[INFO] Artists loaded!"
        
    @commit_on_success
    def loadAlbums():
        
        print "[INFO] Loading albums..."
        
        num_lines = sum(1 for line in open('dataset/albums.csv')) #@UnusedVariable
        
        print "[INFO] Detected " + str(num_lines) + " items"
        
        conn = sqlite3.connect('sqlite.db')
        conn.text_factory = str
        
        with codecs.open('dataset/albums.csv', 'r', encoding='iso-8859-15') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # (id,name,label,genre,styles,release_date,cover_image,duration)
            for row in reader:
                try:
                    artistId = row[0]
                    albumId = row[1]
                    name = row[2]
                    label = row[3]
                    genre = row[4]
                    styles = row[5]
                    try:
                        if len(row[6])==4:
                            releaseDateFormat = "%Y"
                        elif re.match(r'\w+ \d+, \d{4}',row[6]):
                            releaseDateFormat = "%B %d, %Y"
                        else:
                            releaseDateFormat = "%B, %Y"
                        release_date = datetime.datetime.strptime(row[6], releaseDateFormat)
                    except:
                        if detailed:
                            print "[WARNING] The release date of album '" + name + "' has failed when casting."
                        release_date = None
                    cover_image = row[7]
                    try:
                        if row[8].count(":")==2:
                            durationFormat = "%H:%M:%S"
                        else:
                            durationFormat = "%M:%S"
                        duration = datetime.datetime.strptime(row[8], durationFormat)
                    except:
                        if detailed and len(row[8])>0:
                            print "[WARNING] The duration of album '" + name + "' has failed when casting."
                        duration = None
                    
                    conn.execute("INSERT INTO principal_album (id,Nombre,Etiqueta,Generos,Estilos,FechaPublicacion,ImagenPortada,Duracion,Artista_id) VALUES (?,?,?,?,?,?,?,?,?)", (albumId,name,label,genre,styles,release_date,cover_image,duration,artistId))
                except:
                    if detailed:
                        print "[WARNING] The album [" + ';'.join(row) + "] has not been considered."
        
        conn.commit()
        conn.close()
                        
        print "[INFO] Albums loaded!"
        
    @commit_on_success
    def loadSongs():
        
        print "[INFO] Loading songs..."
        
        num_lines = sum(1 for line in open('dataset/songs.csv')) #@UnusedVariable
        
        print "[INFO] Detected " + str(num_lines) + " items"
        
        conn = sqlite3.connect('sqlite.db')
        conn.text_factory = str
        
        with codecs.open('dataset/songs.csv', 'r', encoding='iso-8859-15') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # (id,track_number,name,duration,genre,styles,video_id)
            for row in reader:
                try:
                    albumId = row[0]
                    songId = row[1]
                    track_number = row[2]
                    name = row[3]
                    try:
                        if row[4].count(":")==2:
                            durationFormat = "%H:%M:%S"
                        else:
                            durationFormat = "%M:%S"
                        duration = datetime.datetime.strptime(row[4], durationFormat)
                    except:
                        if detailed and len(row[4])>0:
                            print "[WARNING] The duration of song '" + name + "' has failed when casting."
                        duration = None
                    genre = row[5]
                    styles = row[6]
                    video_id = row[7]
                    
                    conn.execute("INSERT INTO principal_cancion (id,NumeroCancion,Nombre,EnlaceYouTube,Generos,Estilos,Duracion,Album_id) VALUES (?,?,?,?,?,?,?,?)", (songId,track_number,name,video_id,genre,styles,duration,albumId))
                except:
                    if detailed:
                        print "[WARNING] The song [" + ';'.join(row) + "] has not been considered."
        
        conn.commit()
        conn.close()
                        
        print "[INFO] Songs loaded!"
        
    loadArtists()
    loadAlbums()
    loadSongs()

if __name__ == "__main__":
    load(True)