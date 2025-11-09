# spotifyPlaylistMaker/playlists/utils.py
import requests

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

    url = "https://api.spotify.com/v1/audio-features"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(track_ids)}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching audio features:", response.status_code, response.text)
        return {}

    features = response.json().get("audio_features", [])
    return {f["id"]: f for f in features if f}
