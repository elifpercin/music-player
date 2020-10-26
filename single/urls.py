from django.conf.urls import url

from . import views

app_name = 'single'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.kullanici_giris, name='login'),
    url(r'^logout/$', views.kullanici_cikis, name='logout'),
    url(r'^createAlbum/$', views.create_album, name='create_album'),
    url(r'^sarkilar/(?P<filter_by>[a-zA_Z]+)/$', views.sarkilar, name='sarkilar'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^(?P<album_id>[0-9]+)/createSong/$', views.create_song, name='create_sarki'),
    url(r'^(?P<album_id>[0-9]+)/album_sil/$', views.album_sil, name='album_sil'),
    url(r'^(?P<album_id>[0-9]+)/sarki_sil/(?P<song_id>[0-9]+)/$', views.sarki_sil, name='sarki_sil'),
    url(r'^(?P<album_id>[0-9]+)/favori_album/$', views.favori_album, name='favori_album')
]
