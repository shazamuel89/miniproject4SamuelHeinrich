from django.contrib import admin
from .models import Playlist, Song

class SongInline(admin.TabularInline):
    model = Song
    extra = 4

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'has_songs', 'song_count')
    list_filter = ('created_by',)
    search_fields = ('name', 'description')
    inlines = [SongInline]

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'playlist')