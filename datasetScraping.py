#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Creates a dataset by scraping AllMusic.com

scrape function creates artists.csv, albums.csv and songs.csv files 
accompanied by explanatory README.txt file inside a dataset folder.
Each csv file is fed by scraping www.allmusic.com website,
starting on its www.allmusic.com/genres section. It also uses the
YouTube API to get a video id for each song.
"""

import csv
import os
import re
import time
import urllib2
import sys
try:
    import winsound
except:
    print "### [INFO] Skipping finish sound notification: Couldn't import 'winsound' module"

from bs4 import BeautifulSoup
from datetime import datetime


__author__ = "Carlos Alberto Mata Gil"

__version__ = "3.0"
__email__ = "carmatgil@alum.us.es"
__status__ = "Production"

def scrape(allowedGenresNames=None, finishSoundNotification=False, maxArtistsPerGenre=None, maxAlbumsPerArtist=None, maxSongsPerAlbum=None):
    """Args:
        allowedGenresNames: An optional string or tuple of strings with the name or names of all genres you want to scrap. 
            If not passed, it'll scrape all genres by default.
        finishSoundNotification: An optional boolean. 
            If True, you will receive a 'Beep' sound notification when the web scraping finish. 
            If not passed, it'll take False as default value. 
            Note: This feature might work only on Windows devices.
        maxArtistsPerGenre: An optional integer number that represents the maximum number of artists that will be scraped for each genre. 
            If not passed, it'll scrape all artists by default.
        maxAlbumsPerArtist: An optional integer number that represents the maximum number of albums that will be scraped for each artist. 
            If not passed, it'll scrape all albums by default.
        maxSongsPerAlbum: An optional integer number that represents the maximum number of songs that will be scraped for each album. 
            If not passed, it'll scrape all songs by default.
        
    Returns:
        A tuple of integer numbers representing the number of Genres analyzed and the number of Artists, Albums and Songs stored, in that order.
        For example:

        (21, 925, 2675, 26049)
    """
    
    numberOfGenres = 0
    numberOfArtists = 0
    numberOfAlbums = 0
    numberOfSongs = 0
    
    if not (allowedGenresNames is None or isinstance(allowedGenresNames, basestring) or (isinstance(allowedGenresNames, tuple) and all(isinstance(genreName, basestring) for genreName in allowedGenresNames) ) ):
        print "### [INFO] Skipping 'allowedGenresNames' argument"
        allowedGenresNames = None
    
    if "winsound" in sys.modules and not isinstance(finishSoundNotification, bool):
        print "### [INFO] Skipping 'finishSoundNotification' argument"
        finishSoundNotification = False
    
    if not (maxArtistsPerGenre is None or (not isinstance(maxArtistsPerGenre, bool) and isinstance(maxArtistsPerGenre, int) and maxArtistsPerGenre >= 0) ):
        print "### [INFO] Skipping 'maxArtistsPerGenre' argument"
        maxArtistsPerGenre = None
    
    if not (maxAlbumsPerArtist is None or (not isinstance(maxAlbumsPerArtist, bool) and isinstance(maxAlbumsPerArtist, int) and maxAlbumsPerArtist >= 0) ):
        print "### [INFO] Skipping 'maxAlbumsPerArtist' argument"
        maxAlbumsPerArtist = None
        
    if not (maxSongsPerAlbum is None or (not isinstance(maxSongsPerAlbum, bool) and isinstance(maxSongsPerAlbum, int) and maxSongsPerAlbum >= 0) ):
        print "### [INFO] Skipping 'maxSongsPerAlbum' argument"
        maxSongsPerAlbum = None
    
    YouTubeAPIKey = "" # Please, insert here your YouTube API Key, if not passed it'll save '?' for each song youtube video id
    
    print "### [STARTED] Scraping Artists, Albums and Songs from AllMusic.com"
    start_total_time = time.time()
    
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
    
    artistsFile  = open('dataset/artists.csv', "wb")
    artistsWriter = csv.writer(artistsFile, delimiter=';')
    
    albumsFile  = open('dataset/albums.csv', "wb")
    albumsWriter = csv.writer(albumsFile, delimiter=';')
    
    songsFile  = open('dataset/songs.csv', "wb")
    songsWriter = csv.writer(songsFile, delimiter=';')

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    
    req = urllib2.Request("http://www.allmusic.com/genres", headers=hdr)
    try:
        html = urllib2.urlopen(req)
    except:
        print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
        artistsFile.close()
        albumsFile.close()
        songsFile.close()
        return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
    genresSoup = BeautifulSoup(html, 'html.parser')
    
    print "## [STARTED] Searching for Genres"
    start_time = time.time()
    
    genres = genresSoup.findAll('div', {"class": "genre"})
    
    numberOfGenres = len(genres)
    
    print "## [DONE] (" + str(round(time.time() - start_time,3)) + " secs) Searching for Genres: " + str(numberOfGenres) + " genres found."
    
    for genre in genres:
        genreName = genre("h2")[0]("a")[0].getText()
        genreUrl = genre("a")[0].get("href")
        
        if allowedGenresNames is not None and genreName not in allowedGenresNames:
            print "## [INFO] Skipped genre '" + genreName + "'"
            continue
        
        print "## [STARTED] Analyzing genre '" + genreName + "'"
        start_time = time.time()
        
        req = urllib2.Request(genreUrl + "/artists", headers=hdr)
        try:
            html = urllib2.urlopen(req)
        except:
            print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
            artistsFile.close()
            albumsFile.close()
            songsFile.close()
            return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
        artistsSoup = BeautifulSoup(html, 'html.parser')
        
        artistsContainer = artistsSoup.find("div", {"class": "artist-highlights-container"})
        artists = artistsContainer.findAll(recursive=False)
        
        for artistIndex, artist in enumerate(artists):                                                                                  ### ARTISTS
            if maxArtistsPerGenre is not None and artistIndex >= maxArtistsPerGenre:
                break
            
            artistList = []
            
            artistId = artist("a")[0].get("data-tooltip").split('"')[3][2:]
            artistList.append( artistId )                                                                                               # id
            
            try:
                artistList.append( artist.find("div", {"class": "artist"}).getText().strip().encode("iso-8859-15") )                    # name
            except:
                artistList.append('?')
            
            req = urllib2.Request("http://www.allmusic.com/artist/MN"+artistList[0], headers=hdr)
            try:
                html = urllib2.urlopen(req)
            except:
                print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
                artistsFile.close()
                albumsFile.close()
                songsFile.close()
                return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
            artistSoup = BeautifulSoup(html, 'html.parser')
            
            artistMembersContainer = artistSoup.find("div", {"class": "group-members"})
            if artistMembersContainer is not None:
                artistMembersElements = artistMembersContainer.findAll("span", {"itemprop": "name"})
                try:
                    artistMembers = [x.getText().strip().replace(";","").encode("iso-8859-15") for x in artistMembersElements]
                    artistList.append( ', '.join(artistMembers) )                                                                       # members
                except:
                    artistList.append('?')
            else:
                artistList.append('')
                
            artistGenresContainer = artistSoup.find("div", {"class": "genre"})
            if artistGenresContainer is not None:
                artistGenresElements = artistGenresContainer("a")
                try:
                    artistGenres = [x.getText().replace(";","").encode("iso-8859-15") for x in artistGenresElements]
                    artistList.append( ', '.join(artistGenres) )                                                                        # genre
                except:
                    artistList.append('?')
            else:
                artistList.append('')
                
            artistStylesContainer = artistSoup.find("div", {"class": "styles"})
            if artistStylesContainer is not None:
                artistStylesElements = artistStylesContainer("a")
                try:
                    artistStyles = [x.getText().replace(";","").encode("iso-8859-15") for x in artistStylesElements]
                    artistList.append( ', '.join(artistStyles) )                                                                        # styles
                except:
                    artistList.append('?')
            else:
                artistList.append('')
            
            artistPhotoContainer = artistSoup.find("img", {"itemprop": "image"})
            if artistPhotoContainer is not None:
                try:
                    artistList.append( artistPhotoContainer.get("src").encode("iso-8859-15") )                                          # photo
                except:
                    artistList.append('?')
            else:
                artistList.append('')
            
            artistsWriter.writerow(artistList)
            numberOfArtists += 1
            
            print "# [INFO] Analyzing artist '" + artistList[1] + "'"
            
            req = urllib2.Request("http://www.allmusic.com/artist/MN"+artistId+"/discography", headers=hdr)
            try:
                html = urllib2.urlopen(req)
            except:
                print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
                artistsFile.close()
                albumsFile.close()
                songsFile.close()
                return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
            albumsSoup = BeautifulSoup(html, 'html.parser')
            
            try:
                albumsContainer = albumsSoup("tbody")[0]
            except:
                continue # This happens when an artist has only singles
            albums = albumsContainer.findAll(recursive=False)
             
            for albumIndex, album in enumerate(albums):                                                                                 ### ALBUMS
                if maxAlbumsPerArtist is not None and albumIndex >= maxAlbumsPerArtist:
                    break
                
                albumList = []
                 
                albumList.append( artistId )
                 
                albumId = album("a")[0].get("data-tooltip").split('"')[3][2:]
                albumList.append( albumId )                                                                                             # id
                 
                try:
                    albumList.append( album.find("td", {"class": "title"}).get("data-sort-value").encode("iso-8859-15") )               # name
                except:
                    albumList.append('?')
                     
                try:
                    albumList.append( album.find("td", {"class": "label"}).getText().strip().encode("iso-8859-15") )                    # label
                except:
                    albumList.append('?')
                
                req = urllib2.Request("http://www.allmusic.com/album/MW"+albumId, headers=hdr)
                try:
                    html = urllib2.urlopen(req)
                except:
                    print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
                    artistsFile.close()
                    albumsFile.close()
                    songsFile.close()
                    return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
                albumSoup = BeautifulSoup(html, 'html.parser')
                 
                albumGenresContainer = albumSoup.find("div", {"class": "genre"})
                if albumGenresContainer is not None:
                    albumGenresElements = albumGenresContainer("a")
                    try:
                        albumGenres = [x.getText().replace(";","").encode("iso-8859-15") for x in albumGenresElements]
                        albumList.append( ', '.join(albumGenres) )                                                                      # genre
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                 
                albumStylesContainer = albumSoup.find("div", {"class": "styles"})
                if albumStylesContainer is not None:
                    albumStylesElements = albumStylesContainer("a")
                    try:
                        albumStyles = [x.getText().replace(";","").encode("iso-8859-15") for x in albumStylesElements]
                        albumList.append( ', '.join(albumStyles) )                                                                      # styles
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                 
                albumReleaseDateContainer = albumSoup.find("div", {"class": "release-date"})
                if albumReleaseDateContainer is not None:
                    try:
                        albumList.append( albumReleaseDateContainer("span")[0].getText().encode("iso-8859-15") )                        # release date
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                 
                try:
                    albumList.append( albumSoup.find("div", {"class": "album-contain"})("img")[0].get("src").encode("iso-8859-15") )    # cover image
                except:
                    albumList.append('?')
                 
                albumDurationContainer = albumSoup.find("div", {"class": "duration"})
                if albumDurationContainer is not None:
                    try:
                        albumList.append( albumDurationContainer("span")[0].getText().encode("iso-8859-15") )                           # duration
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                     
                albumsWriter.writerow(albumList)
                numberOfAlbums += 1
                
                req = urllib2.Request("http://www.allmusic.com/album/MW"+albumId, headers=hdr)
                try:
                    html = urllib2.urlopen(req)
                except:
                    print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
                    artistsFile.close()
                    albumsFile.close()
                    songsFile.close()
                    return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
                songsSoup = BeautifulSoup(html, 'html.parser')
                  
                songs = songsSoup.findAll("tr", {"class": "track"})
                  
                for songIndex, song in enumerate(songs):                                                                                ### SONGS
                    if maxSongsPerAlbum is not None and songIndex >= maxSongsPerAlbum:
                        break
                    
                    songList = []
                  
                    songList.append( albumId )
                     
                    songUrlElement = song.find("a", {"itemprop": "url"})
                     
                    if songUrlElement is None:
                        break # When the album is a film soundtrack album, it has performances, not songs
                      
                    songId = songUrlElement.get("href").split("-")[-1][2:]
                    songList.append( songId )                                                                                           # id
                     
                    songList.append( song.find("td", {"class": "tracknum"}).getText().strip().encode("iso-8859-15") )                   # track number
                     
                    try:
                        songList.append( songUrlElement.getText().encode("iso-8859-15") )                                               # name
                    except:
                        songList.append('?')
                     
                    songList.append( song.find("td", {"class": "time"}).getText().strip().encode("iso-8859-15") )                       # duration
                    
                    req = urllib2.Request("http://www.allmusic.com/song/MT"+albumId, headers=hdr)
                    try:
                        html = urllib2.urlopen(req)
                    except:
                        print "### [STOPPED] Scraping Artists, Albums and Songs from AllMusic.com: Unable to connect to http://www.allmusic.com, please check you Internet connection and try it again."
                        artistsFile.close()
                        albumsFile.close()
                        songsFile.close()
                        return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
                    songSoup = BeautifulSoup(html, 'html.parser')
                     
                    songGenresContainer = songSoup.find("div", {"class": "genre"})
                    if songGenresContainer is not None:
                        songGenresElements = songGenresContainer("a")
                        try:
                            songGenres = [x.getText().replace(";","").encode("iso-8859-15") for x in songGenresElements]
                            songList.append( ', '.join(songGenres) )                                                                    # genre
                        except:
                            songList.append('?')
                    else:
                        songList.append('')
                     
                    songStylesContainer = songSoup.find("div", {"class": "styles"})
                    if songStylesContainer is not None:
                        songStylesElements = songStylesContainer("a")
                        try:
                            songStyles = [x.getText().replace(";","").encode("iso-8859-15") for x in songStylesElements]
                            songList.append( ', '.join(songStyles) )                                                                    # styles
                        except:
                            songList.append('?')
                    else:
                        songList.append('')
                    
                    try:
                        req = urllib2.Request("https://www.googleapis.com/youtube/v3/search?part=snippet&q="+songList[3].replace(" ","+")+"+"+artistList[1].replace(" ","+")+"&type=video&key="+YouTubeAPIKey, headers=hdr)
                        response = urllib2.urlopen(req)
                        html = response.read()
                        songYouTubeVideoId = re.findall(r'"videoId": "(.+)"',html)[0]
                        songList.append(songYouTubeVideoId)                                                                             # youtube video id
                    except:
                        songList.append("?")
                    
                    songsWriter.writerow(songList)
                    numberOfSongs += 1
        
        print "## [DONE] (" + str(round(time.time() - start_time,3)) + " secs) Analyzing genre '" + genreName + "'"
    
    artistsFile.close()
    albumsFile.close()
    songsFile.close()
    
    print "### [DONE] (" + str(round(time.time() - start_total_time,3)) + " secs) Scraping Artists, Albums and Songs from AllMusic.com"
    
    if "winsound" in sys.modules and finishSoundNotification:
        Freq = 2500 # Frequency in Hertz
        Dur = 500 # Duration in ms
        winsound.Beep(Freq,Dur)
        
    return (numberOfGenres, numberOfArtists, numberOfAlbums, numberOfSongs)
        
def generateReadmeFile(dataStatistics):
    """Generates a README.txt file with information about the dataset .csv files
    
    This function generates a README.txt on dataset folder in which it is
    explained where were all data retrieved from and what's the meaning of
    each column for each .csv file.
    
    Args:
        dataStatistics: A tuple of integer numbers representing the number of Genres analyzed and the number of Artists, Albums and Songs stored, in that order.
    """
    
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
        
    readmeFile  = open('dataset/README.txt', "w")
    
    readmeContent = """
=======
dataset
=======

-------
Version
-------

Version {version} ({date})

-----------
Description
-----------

    This dataset contains music artists, albums and songs information 
    retrieved from performing web scraping on http://www.allmusic.com

    The dataset was created for a college work for the subject
    'Acceso Inteligente a la Información' of the department
    'Lenguajes y Sistemas Informáticos' on the degree 'Ingeniería 
    Informática del Software' of the University of Seville, Spain.

---------------
Data statistics
---------------

   genres* {numberOfGenres}
   artists {numberOfArtists}
    albums {numberOfAlbums}
     songs {numberOfSongs}
     
   *genres just represent the number of analyzed genres, but 
   there isn't an specific .csv file for storing their 
   information.

-----
Files
-----

   * artists.csv
   
        This file contains information about music artists of every analyzed genre.
        
   * albums.csv
   
        This file contains information about albums of every analyzed artists.
        
   * songs.csv
   
        This file contains information about songs of every analyzed albums.
    
-----------
Data format
-----------

   The data is formatted one entry per line as follows (semicolon separated, ";"):

   * artists.csv
   
        id;name;members;genre;styles;photo

        Example:
        0000074616;Borbetomagus;Donald Dietrich, Donald Miller, Jim Sauter;Avant-Garde, Jazz;Free Improvisation, Fusion, Noise;http://cps-static.rovicorp.com/3/JPG_400/MI0003/150/MI0003150663.jpg?partner=allrovi.com

   * albums.csv
 
        artistId;id;name;label;genre;styles;releaseDate;coverImage;duration
        0000664817;0000650124;Let It Loose;Epic;Pop/Rock;Dance-Pop, Latin Pop, Contemporary Pop/Rock;June 2, 1987;http://cdn-s3.allmusic.com/release-covers/500/0000/280/0000280376.jpg;38:09
 
   * songs.csv
   
        albumId;id;trackNumber;name;duration;genre;styles;youtubeVideoId
        0000653824;0005944471;3;Say;3:41;Latin, Jazz, International;Latin Jazz, World Fusion, Brazilian Traditions;TBOvPBvQP3o

"""
    
    context = {
        "numberOfGenres": dataStatistics[0], 
        "numberOfArtists": dataStatistics[1],
        "numberOfAlbums": dataStatistics[2],
        "numberOfSongs": dataStatistics[3],
        "version": __version__,
        "date": datetime.now().strftime('%Y-%m-%d')
    }
    
    readmeFile.write(readmeContent.format(**context))
    
    readmeFile.close()
    
    print "### [INFO] README.txt generated"

if __name__ == '__main__':
    dataStatistics = scrape()
    generateReadmeFile(dataStatistics)
