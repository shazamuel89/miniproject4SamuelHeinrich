# playlists/utils.py
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.providers.spotify.views import SpotifyOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp
import requests
from django.utils import timezone

def get_user_playlists(access_token):
    # Fetch user's playlists from Spotify API.
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    playlists = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Error fetching playlists:", response.status_code, response.text)
            break

        data = response.json()
        playlists.extend(data["items"])
        url = data.get("next")  # pagination support

    return playlists


def get_playlist_tracks(access_token, playlist_id):
    # Fetch all tracks (and their tags) from a Spotify playlist.
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Error fetching tracks:", response.status_code, response.text)
            break

        data = response.json()
        tracks.extend(data["items"])
        url = data.get("next")  # pagination support

    return tracks


def get_audio_features(access_token, track_ids):
    # Fetch audio features (tags like energy, danceability, etc.) for multiple tracks.
    if not track_ids:
        return {}

    # Filter out None or empty values
    valid_ids = [tid for tid in track_ids if tid]
    if not valid_ids:
        return {}

    url = "https://api.spotify.com/v1/audio-features"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(track_ids)}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        try:
            error_info = response.json()
            print("Error fetching audio features:", response.status_code, error_info)
        except Exception:
            print("Error fetching audio features:", response.status_code, response.text)
        return {}

    features = response.json().get("audio_features", [])
    return {f["id"]: f for f in features if f}


def get_valid_spotify_token(user):
    token = SocialToken.objects.filter(account__user=user, account__provider='spotify').first()

    if not token:
        raise Exception("No Spotify token found for user")

    # Check if token is expired
    if token.expires_at and token.expires_at <= timezone.now():
        # Refresh it
        app = SocialApp.objects.get(provider='spotify')
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': token.token_secret,
            },
            auth=(app.client_id, app.secret),
        )
        data = response.json()
        token.token = data['access_token']
        token.expires_at = timezone.now() + timezone.timedelta(seconds=data['expires_in'])
        token.save()

    return token.token
