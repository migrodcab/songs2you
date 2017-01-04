from principal.models import Artista, Album, Cancion

def todosLosGeneros(tipo):
    lista = []
    if tipo == "cancion":
        lista = Cancion.objects.all()
        
    if tipo == "album":
        lista = Album.objects.all()
        
    if tipo == "artista":
        lista = Artista.objects.all()
        
    generos = []
    for item in lista:
        generosAux = item.Generos.split(', ')
        for genero in generosAux:
            if generos.__contains__(genero) == False:
                generos.append(genero)

    generos.sort()
    return generos