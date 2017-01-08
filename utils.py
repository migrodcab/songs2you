#encoding:utf-8
from principal.models import Artista, Cancion, Album

def allGenres(entity):
    items = []
    if entity == "song":
        items = Cancion.objects.all()
        
    if entity == "album":
        items = Album.objects.all()
        
    if entity == "artist":
        items = Artista.objects.all()
        
    genres = []
    for item in items:
        tokenizedGenres = item.Generos.split(', ')
        for genre in tokenizedGenres:
            if genres.__contains__(genre) == False:
                genres.append(genre)

    genres.sort()
    return genres

def pagination(paginator, page):
    try:
        data1 = None
        data2 = None
        data3 = None
        data4 = None
        data5 = None
        data6 = None
        data7 = None
        data8 = None
        data9 = None
        data10 = None
        
        data = paginator.page(page)
        aaa=data
        num_pages = paginator.page(paginator.num_pages).number
    
        if data.number - 5 >= 1:
            data1 =  paginator.page(data.number - 5).number
        if data.number - 4 >= 1:
            data2 =  paginator.page(data.number - 4).number
        if data.number - 3 >= 1:
            data3 =  paginator.page(data.number - 3).number
        if data.number - 2 >= 1:
            data4 =  paginator.page(data.number - 2).number
        if data.number - 1 >= 1:
            data5 =  paginator.page(data.number - 1).number
        if data.number + 1 <= num_pages:
            data6 =  paginator.page(data.number + 1).number
        if data.number + 2 <= num_pages:
            data7 =  paginator.page(data.number + 2).number
        if data.number + 3 <= num_pages:
            data8 =  paginator.page(data.number + 3).number
        if data.number + 4 <= num_pages:
            data9 =  paginator.page(data.number + 4).number
        if data.number + 5 <= num_pages:
            data10 =  paginator.page(data.number + 5).number
        print data
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        
    print data
    return (data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10)