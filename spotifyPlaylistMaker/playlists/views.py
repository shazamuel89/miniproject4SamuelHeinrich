# spotifyPlaylistMaker/playlists/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Playlist, Song
from .forms import PlaylistForm


def index(request):
    # Home page that shows all created playlists from all users.
    playlists = Playlist.objects.all()
    return render(request, 'playlists/index.html', {'playlists': playlists})

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'playlists/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class MyPlaylistsView(LoginRequiredMixin, generic.ListView):
    model = Playlist
    template_name = 'playlists/my_playlists.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        # Limit to logged in user's playlists
        return Playlist.objects.filter(created_by=self.request.user)

class PlaylistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'playlists/playlist_detail.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        # Limit access to user's own playlists
        return Playlist.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()
        return context

    def get_success_url(self):
        return reverse('playlist_detail', kwargs={'pk': self.object.pk})

class SongDetailView(LoginRequiredMixin, generic.DetailView):
    model = Song
    template_name = 'playlists/song_detail.html'
    context_object_name = 'song'