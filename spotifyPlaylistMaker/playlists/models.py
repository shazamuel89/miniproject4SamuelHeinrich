from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Spotify integration fields
    spotify_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    @admin.display(boolean=True, description='Has songs?')
    def has_songs(self):
        return self.songs.exists()

    @admin.display(description='Song count')
    def song_count(self):
        return self.songs.count()


class Song(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100, blank=True)

    # Spotify track reference
    spotify_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.artist}'
