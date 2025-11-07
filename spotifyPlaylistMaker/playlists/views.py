# spotifyPlaylistMaker/playlists/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Playlist, Song
from .forms import PlaylistForm, SongForm


def index(request):
    '''Login or home page.'''
    return render(request, 'playlists/index.html')


@login_required
def profile(request):
    user_playlists = Playlist.objects.filter(created_by=request.user)
    total_songs = Song.objects.filter(playlist__created_by=request.user).count()
    context = {'user': request.user, 'playlists': user_playlists, 'total_songs': total_songs}
    return render(request, 'playlists/profile.html', context)


class PlaylistListView(generic.ListView):
    model = Playlist
    template_name = 'playlists/playlist_list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        # Limit to logged in user's playlists
        return Playlist.objects.filter(created_by=self.request.user)


class PlaylistDetailView(generic.DetailView):
    model = Playlist
    template_name = 'playlists/playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()
        return context


class SongDetailView(generic.DetailView):
    model = Song
    template_name = 'playlists/song_detail.html'
    context_object_name = 'song'
