from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','principal.views.index'),
    url(r'^canciones/$','principal.views.canciones'),
    url(r'^canciones/(?P<genero>.*)$','principal.views.canciones'),
    url(r'^albumes/$','principal.views.albumes'),
    url(r'^albumes/(?P<genero>.*)$','principal.views.albumes'),
    url(r'^artistas/$','principal.views.artistas'),
    url(r'^artistas/(?P<genero>.*)$','principal.views.artistas'),
    url(r'^album/(?P<albumId>\d+)$','principal.views.displayAlbum'),
    url(r'^artist/(?P<artistId>\d+)$','principal.views.displayArtist'),
    url(r'^$','principal.views.index'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),
)