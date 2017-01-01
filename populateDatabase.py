#encoding:iso-8859-15

'''
Created on 30/12/2016

@author: Javier Garcia (javgarcal@alum.us.es)
'''
import datetime

from principal.models import Artista, Album, Cancion


arctic_monkeys = Artista.objects.create(Nombre="Arctic Monkeys",Miembros="Alex Turner, Matt Helders, Jamie Cook, Nick O'Malley, Andy Nicholson, Glyn Jones",Generos="Indie rock, Garage rock, Post punk revival, Rock psicodelico")
am = Album.objects.create(Nombre="AM",FechaPublicacion=datetime.datetime.strptime("09-09-2013", "%d-%m-%Y"),Generos="Rock, Indie rock, Britpop, Rock psicodelico, Garage rock, Hard rock",ImagenPortada="https://images-na.ssl-images-amazon.com/images/I/71hEtk3aCpL._SL1500_.jpg",Artista=arctic_monkeys)
do_i_wanna_know = Cancion.objects.create(Nombre="Do I Wanna Know?",EnlaceYouTube="bpOSxM0rNPM",Album=am)
r_u_mine = Cancion.objects.create(Nombre="R U Mine?",EnlaceYouTube="VQH8ZTgna3Q",Album=am)
one_for_the_road = Cancion.objects.create(Nombre="One For The Road",EnlaceYouTube="qN7gSMPQFss",Album=am)
suck_it_and_see = Album.objects.create(Nombre="Suck It And See",FechaPublicacion=datetime.datetime.strptime("06-06-2011", "%d-%m-%Y"),Generos="Indie rock, Pop, Rock alternativo, Rock psicodelico",ImagenPortada="http://2.bp.blogspot.com/-npTe8vMA_s4/Ub-JczFTjSI/AAAAAAAABVY/X_RhPz-lvY8/s1600/Arctic+Monkeys+-+Suck+It+And+See.jpg",Artista=arctic_monkeys)
shes_thunderstorms = Cancion.objects.create(Nombre="She's Thunderstorms",EnlaceYouTube="ZQTsKxd0_1k",Album=suck_it_and_see)
black_treacle = Cancion.objects.create(Nombre="Black Treacle",EnlaceYouTube="1wznj4lD1Bs",Album=suck_it_and_see)

the_kooks = Artista.objects.create(Nombre="The Kooks",Miembros="Luke Pritchard, Hugh Harris, Max Rafferty, Paul Garred, Peter Denton, Dan Logan",Generos="Indie rock, Post-britpop, Rock alternativo, Indie pop, Post punk revival")
inside_in_inside_out = Album.objects.create(Nombre="Inside In/Inside Out",FechaPublicacion=datetime.datetime.strptime("26-01-2006", "%d-%m-%Y"),Generos="Indie rock, Britpop, Rock alternativo, Post-britpop",ImagenPortada="http://www.elrocknomuere.com/blog/img/albums/inside+ininside+out.jpg",Artista=the_kooks)
seaside = Cancion.objects.create(Nombre="Seaside",EnlaceYouTube="7_RZLAxsa8Q",Album=inside_in_inside_out)