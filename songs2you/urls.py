from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','principal.views.index'),
    url(r'^songs/$','principal.views.songs'),
    url(r'^songs/genre/(?P<genre>.*)$','principal.views.songs'),
    url(r'^songs/playlist/(?P<playlist>.*)$','principal.views.songs'),
    url(r'^albums/$','principal.views.albums'),
    url(r'^albums/(?P<genre>.*)$','principal.views.albums'),
    url(r'^artists/$','principal.views.artists'),
    url(r'^artists/(?P<genre>.*)$','principal.views.artists'),
    url(r'^album/(?P<albumId>\d+)$','principal.views.displayAlbum'),
    url(r'^artist/(?P<artistId>\d+)$','principal.views.displayArtist'),
    url(r'^user/new$','principal.views.newUser'),
    url(r'^login/$','principal.views.loginUser'),
    url(r'^userindex/$','principal.views.userIndex'),
    url(r'^logout/$','principal.views.logoutUser'),
    url(r'^playlists/$','principal.views.playlists'),
    url(r'^playlist/new/$','principal.views.newPlaylist'),
    url(r'^$','principal.views.index'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
    ),
)