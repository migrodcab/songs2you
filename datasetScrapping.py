#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Creates a dataset by scrapping AllMusic.com

scrap function creates artists.csv, albums.csv and songs.csv files 
accompanied by explanatory README.txt file inside a dataset folder.
Each csv file is fed by scrapping www.allmusic.com website,
starting on its www.allmusic.com/genres section.
"""

import csv
import os
import re
import time
import urllib2

from bs4 import BeautifulSoup


__author__ = "Carlos Alberto Mata Gil"

__version__ = "1.1"
__email__ = "carmatgil@alum.us.es"
__status__ = "Production"

def scrap(allowedGenres=None):
    
    YouTubeAPIKey = ""
    
    print "### [STARTED] Scrapping Artists, Albums and Songs from AllMusic.com"
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
    html = urllib2.urlopen(req)
    
    genresSoup = BeautifulSoup(html, 'html.parser')
    
    print "## [STARTED] Searching for Genres"
    start_time = time.time()
    
    genres = genresSoup.findAll('div', {"class": "genre"})
    
    print "## [DONE] (" + str(round(time.time() - start_time,3)) + " secs) Searching for Genres: " + str(len(genres)) + " genres found."
    
    for genre in genres:
        genreName = genre("h2")[0]("a")[0].getText()
        genreUrl = genre("a")[0].get("href")
        
        if type(allowedGenres) != type(None) and genreName not in allowedGenres:
            print "## [INFO] Skipped genre '" + genreName + "'"
            continue
        
        print "## [STARTED] Analyzing genre '" + genreName + "'"
        start_time = time.time()
        
        req = urllib2.Request(genreUrl + "/artists", headers=hdr)
        html = urllib2.urlopen(req)
        artistsSoup = BeautifulSoup(html, 'html.parser')
        
        artistsContainer = artistsSoup.find("div", {"class": "artist-highlights-container"})
        artists = artistsContainer.findAll(recursive=False)
        
        for artist in artists:                                                                                                          ### ARTISTS
            artistList = []
            
            artistId = artist("a")[0].get("data-tooltip").split('"')[3][2:]
            artistList.append( artistId )                                                                                               # id
            
            try:
                artistList.append( artist.find("div", {"class": "artist"}).getText().strip().encode("iso-8859-15") )                    # name
            except:
                artistList.append('?')
            
            req = urllib2.Request("http://www.allmusic.com/artist/MN"+artistList[0], headers=hdr)
            html = urllib2.urlopen(req)
            artistSoup = BeautifulSoup(html, 'html.parser')
            
            artistMembersContainer = artistSoup.find("div", {"class": "group-members"})
            if artistMembersContainer != None:
                artistMembersElements = artistMembersContainer.findAll("span", {"itemprop": "name"})
                try:
                    artistMembers = [x.getText().strip().encode("iso-8859-15") for x in artistMembersElements]
                    artistList.append( ', '.join(artistMembers) )                                                                       # members
                except:
                    artistList.append('?')
            else:
                artistList.append('')
                
            artistGenresContainer = artistSoup.find("div", {"class": "genre"})
            if artistGenresContainer != None:
                artistGenresElements = artistGenresContainer("a")
                try:
                    artistGenres = [x.getText().encode("iso-8859-15") for x in artistGenresElements]
                    artistList.append( ', '.join(artistGenres) )                                                                        # genre
                except:
                    artistList.append('?')
            else:
                artistList.append('')
                
            artistStylesContainer = artistSoup.find("div", {"class": "styles"})
            if artistStylesContainer != None:
                artistStylesElements = artistStylesContainer("a")
                try:
                    artistStyles = [x.getText().encode("iso-8859-15") for x in artistStylesElements]
                    artistList.append( ', '.join(artistStyles) )                                                                        # styles
                except:
                    artistList.append('?')
            else:
                artistList.append('')
            
            try:
                artistList.append( artistSoup.find("img", {"itemprop": "image"}).get("src").encode("iso-8859-15") )                     # photo
            except:
                artistList.append('?')
            
            artistsWriter.writerow(artistList)
            print "## [INFO] Analyzing artist '" + artistList[1] + "'"
            
            req = urllib2.Request("http://www.allmusic.com/artist/MN"+artistId+"/discography", headers=hdr)
            html = urllib2.urlopen(req)
            albumsSoup = BeautifulSoup(html, 'html.parser')
             
            albumsContainer = albumsSoup("tbody")[0]
            albums = albumsContainer.findAll(recursive=False)
             
            for index, album in enumerate(albums):                                                                                      ### ALBUMS
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
                html = urllib2.urlopen(req)
                albumSoup = BeautifulSoup(html, 'html.parser')
                 
                albumGenresContainer = albumSoup.find("div", {"class": "genre"})
                if albumGenresContainer != None:
                    albumGenresElements = albumGenresContainer("a")
                    try:
                        albumGenres = [x.getText().encode("iso-8859-15") for x in albumGenresElements]
                        albumList.append( ', '.join(albumGenres) )                                                                      # genre
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                 
                albumStylesContainer = albumSoup.find("div", {"class": "styles"})
                if albumStylesContainer != None:
                    albumStylesElements = albumStylesContainer("a")
                    try:
                        albumStyles = [x.getText().encode("iso-8859-15") for x in albumStylesElements]
                        albumList.append( ', '.join(albumStyles) )                                                                      # styles
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                 
                albumReleaseDateContainer = albumSoup.find("div", {"class": "release-date"})
                if albumReleaseDateContainer != None:
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
                if albumDurationContainer != None:
                    try:
                        albumList.append( albumDurationContainer("span")[0].getText().encode("iso-8859-15") )                           # duration
                    except:
                        albumList.append('?')
                else:
                    albumList.append('')
                     
                albumsWriter.writerow(albumList)
                 
                req = urllib2.Request("http://www.allmusic.com/album/MW"+albumId, headers=hdr)
                html = urllib2.urlopen(req)
                songsSoup = BeautifulSoup(html, 'html.parser')
                  
                songs = songsSoup.findAll("tr", {"class": "track"})
                  
                for song in songs:                                                                                                      ### SONGS
                    songList = []
                  
                    songList.append( albumId )
                     
                    songUrlElement = song.find("a", {"itemprop": "url"})
                     
                    if songUrlElement == None:
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
                    html = urllib2.urlopen(req)
                    songSoup = BeautifulSoup(html, 'html.parser')
                     
                    songGenresContainer = songSoup.find("div", {"class": "genre"})
                    if songGenresContainer != None:
                        songGenresElements = songGenresContainer("a")
                        try:
                            songGenres = [x.getText().encode("iso-8859-15") for x in songGenresElements]
                            songList.append( ', '.join(songGenres) )                                                                    # genre
                        except:
                            songList.append('?')
                    else:
                        songList.append('')
                     
                    songStylesContainer = songSoup.find("div", {"class": "styles"})
                    if songStylesContainer != None:
                        songStylesElements = songStylesContainer("a")
                        try:
                            songStyles = [x.getText().encode("iso-8859-15") for x in songStylesElements]
                            songList.append( ', '.join(songStyles) )                                                                    # styles
                        except:
                            songList.append('?')
                    else:
                        songList.append('')
                    
                    try:
                        req = urllib2.Request("https://www.googleapis.com/youtube/v3/search?part=snippet&q="+songList[3].replace(" ","+")+"+"+artistList[1].replace(" ","+")+"&type=video&key="+YouTubeAPIKey, headers=hdr)
                        response = urllib2.urlopen(req)
                        html = response.read()
                        songYouTubeURL = re.findall(r'"videoId": "(.+)"',html)[0]
                        songList.append(songYouTubeURL)
                    except:
                        songList.append("?")
                    
                    songsWriter.writerow(songList)
                     
                if index == 2: # It sets a limit of 3 albums per artist due to a huge amount of albums and songs of some artists
                    break
        
        print "## [DONE] (" + str(round(time.time() - start_time,3)) + " secs) Analyzing genre '" + genreName + "'"
    
    artistsFile.close()
    albumsFile.close()
    songsFile.close()
    
    print "### [DONE] (" + str(round(time.time() - start_total_time,3)) + " secs) Scrapping Artists, Albums and Songs from AllMusic.com"
    
if __name__ == '__main__':
    allowedGenres = ("Pop/Rock")
    scrap(allowedGenres)
