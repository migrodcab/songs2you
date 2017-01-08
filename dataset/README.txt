
=======
dataset
=======

-------
Version
-------

Version 3.0 (2017-01-08)

-----------
Description
-----------

    This dataset contains music artists, albums and songs information 
    retreived from using web scraping on http://www.allmusic.com

    The dataset was created for a college work for the subject
    'Acceso Inteligente a la Información' of the department
    'Lenguajes y Sistemas Informáticos' on the degree 'Ingeniería 
    Informática del Software' of the University of Seville, Spain.

---------------
Data statistics
---------------

   genres* 21
   artists 925
    albums 2675
     songs 26049
     
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

