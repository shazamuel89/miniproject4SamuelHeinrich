# spotifyPlaylistMaker/playlists/urls.py
from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('my_playlists/', views.MyPlaylistsView.as_view(), name='my_playlists'),
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
]
