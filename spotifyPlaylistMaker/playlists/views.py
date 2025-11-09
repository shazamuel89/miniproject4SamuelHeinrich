# spotifyPlaylistMaker/playlists/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from allauth.socialaccount.models import SocialToken
from .models import Playlist, Song
from .forms import PlaylistForm
from .utils import get_user_playlists, get_playlist_tracks, get_audio_features
from django.urls import reverse


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
            token = SocialToken.objects.get(account__user=self.request.user, account__provider='spotify')
            access_token = token.token

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
            token = SocialToken.objects.get(account__user=self.request.user, account__provider='spotify')
            access_token = token.token

            # Fetch songs from Spotify
            spotify_tracks = get_playlist_tracks(access_token, playlist.spotify_id)

            # Store them locally
            track_ids = []
            for item in spotify_tracks:
                track = item['track']
                if track:  # sometimes null
                    track_ids.append(track['id'])
                    Song.objects.update_or_create(
                        spotify_id=track['id'],
                        defaults={
                            'playlist': playlist,
                            'title': track['name'],
                            'artist': ', '.join(artist['name'] for artist in track['artists']),
                            'album': track['album']['name'],
                        }
                    )

            # Fetch and store audio features (energy, danceability, etc.)
            features = get_audio_features(access_token, track_ids)
            for song in Song.objects.filter(playlist=playlist):
                f = features.get(song.spotify_id)
                if f:
                    song.energy = f.get('energy')
                    song.danceability = f.get('danceability')
                    song.valence = f.get('valence')
                    song.tempo = f.get('tempo')
                    song.save()

        except SocialToken.DoesNotExist:
            context['error'] = "Spotify account not connected."

        context['songs'] = Song.objects.filter(playlist=playlist)
        return context

    def get_success_url(self):
        return reverse('playlist_detail', kwargs={'pk': self.object.pk})

class SongDetailView(LoginRequiredMixin, generic.DetailView):
    model = Song
    template_name = 'playlists/song_detail.html'
    context_object_name = 'song'