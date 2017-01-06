from principal.models import Artista, Album, Cancion

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