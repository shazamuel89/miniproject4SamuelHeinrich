from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from allauth.socialaccount.models import SocialToken
from django.urls import reverse_lazy, reverse
from .models import Playlist, Song
from .forms import PlaylistForm
from .utils import get_user_playlists, get_playlist_tracks, get_valid_spotify_token


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            access_token = get_valid_spotify_token(self.request.user)

            # Fetch playlists from Spotify
            spotify_playlists = get_user_playlists(access_token)

            # Store or update locally
            for pl in spotify_playlists:
                Playlist.objects.update_or_create(
                    spotify_id=pl['id'],
                    defaults={
                        'name': pl['name'],
                        'description': pl.get('description', ''),
                        'created_by': self.request.user,
                    },
                )

        except SocialToken.DoesNotExist:
            context['error'] = "Spotify account not connected."

        context['playlists'] = Playlist.objects.filter(created_by=self.request.user)
        return context


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
        playlist = self.get_object()

        try:
            access_token = get_valid_spotify_token(self.request.user)

            # Fetch songs from Spotify
            spotify_tracks = get_playlist_tracks(access_token, playlist.spotify_id)

            # Store them locally (without fetching audio features)
            for item in spotify_tracks:
                track = item.get('track')
                if track and track.get('id'):
                    Song.objects.update_or_create(
                        spotify_id=track['id'],
                        defaults={
                            'playlist': playlist,
                            'title': track.get('name'),
                            'artist': ', '.join(artist['name'] for artist in track.get('artists', [])),
                            'album': track.get('album', {}).get('name', ''),
                        }
                    )

        except SocialToken.DoesNotExist:
            context['error'] = "Spotify account not connected."

        context['songs'] = Song.objects.filter(playlist=playlist)
        return context

    def get_success_url(self):
        return reverse('playlists:playlist_detail', kwargs={'pk': self.object.pk})


class PlaylistCreateView(LoginRequiredMixin, generic.CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'playlists/playlist_create.html'
    success_url = reverse_lazy('playlists:my_playlists')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
