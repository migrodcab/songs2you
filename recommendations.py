#encoding:utf-8

'''
Created on 06/12/2016

@author: javgarcal@alum.us.es
'''

from cmath import log
from collections import Counter
import operator, sqlite3, sys, re

from principal.models import Artista


reload(sys)
sys.setdefaultencoding('UTF8')  # @UndefinedVariable

def updateArtistContent():
    conn = sqlite3.connect('sqlite.db')
    conn.text_factory = str
    
    conn.execute('''CREATE TABLE IF NOT EXISTS artistscontent
       (ID        INT    NOT NULL,
       TAG1       TEXT    ,
       TAG2       TEXT    ,
       TAG3       TEXT    ,
       TAG4       TEXT    );''')
    
    artists = Artista.objects.all()
    
    artists_tags = {}
    for artist in artists:
        words = re.findall(r'\w+',artist.Generos + " " + artist.Estilos)
        
        lowercase_words = [word.lower() for word in words]
        
        word_frequency = Counter(lowercase_words)
        
        sorted_word_frequency = sorted(word_frequency.items(), key=operator.itemgetter(1), reverse=True)[:4]
        
        content = [item[0] for item in sorted_word_frequency]
        
        sql = "INSERT INTO artistscontent (ID,TAG1,TAG2,TAG3,TAG4) VALUES (?,?,?,?,?)"
        params = [artist.id]
        for tag in content:
            params += [tag]
        if len(params)<5:
            for i in range(5-len(params)): #@UnusedVariable
                params += [""]
        conn.execute(sql, params)
    
    conn.commit()
    conn.close()
    
    return artists_tags

def getArtistContent():
    conn = sqlite3.connect('sqlite.db')
    conn.text_factory = str
    
    cursor = conn.execute('SELECT * FROM artistscontent')
    
    artists_tags = {}
    for row in cursor:
        artists_tags[row[0]] = [row[i] for i in range(1,5)]
    
    return artists_tags

def getSimpleApproachMetric(artists_tags,user_preferences,key):
    user_keywords = len(user_preferences)
    artist_keywords = len(artists_tags[key])
    common_keywords = len(list(set(user_preferences) & set(artists_tags[key])))
    
    return 2.0*common_keywords/(user_keywords+artist_keywords)

def getTFIDF(artists_tags,user_preferences,key,idf):
    user_preferences = " ".join(user_preferences)
    TF = 0
    IDF = 0 #@UnusedVariable
    N = len(artists_tags)
    ni = 0
    artist_tag = artists_tags[key]
    
    for word in user_preferences.split(" "):
        TF += artist_tag.count(word)
    
    if idf==-1:
        for key in artists_tags.keys():
            ni += len(list(set(user_preferences.split(" ")) & set(artists_tags[key])))
        
        IDF = log(N/float(ni),10)
        IDF = IDF.real
    else:
        IDF = idf
    
    return (TF,IDF)

def getRecommendations(artistId,num,metric):
    artists_tags = getArtistContent()
    user_preferences = artists_tags[artistId]
    
    similarity = {}
    for i,key in enumerate(artists_tags.keys()):
        if metric == 'SimpleApproachMetric':
            similarity[key] = getSimpleApproachMetric(artists_tags, user_preferences, key)
        elif metric == 'TF-IDF':
            if i==0:
                (TF,IDF) = getTFIDF(artists_tags, user_preferences, key, -1)
            else:
                (TF,IDF) = getTFIDF(artists_tags, user_preferences, key, IDF)
            similarity[key] = TF*IDF
        else:
            return Exception("[ERROR] Invalid similarity metric specified")
        
    sorted_similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    
    return sorted_similarity[:num]

if __name__ == "__main__":
    print getRecommendations(467203, 5, "TF-IDF")