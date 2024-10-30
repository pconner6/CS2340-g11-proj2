from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, response
from requests import Request, post
from django.http import HttpResponseRedirect
from django.conf import settings
from ..extras import *

class AuthenticationURL(APIView):
    def get(self, request, format = None):
        scopes = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
        url = Request('GET', 'https://accounts.spotify.com/authorize', params = {
            'scope' : scopes,
            'response_type' : 'code',
            'redirect_uri' : settings.SPOTIFY_REDIRECT_URI,
            'client_id' : settings.SPOTIFY_CLIENT_ID,
        }).prepare().url
        return HttpResponseRedirect(url)

def spotify_redirect(request, format = None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return error

    response = post('https://accounts.spotify.com/api/token', data = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : settings.SPOTIFY_REDIRECT_URI,
        'client_id' : settings.SPOTIFY_CLIENT_ID,
        'client_secret' : settings.SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    authKey = request.session.session_key
    if not request.session.exists(authKey):
        request.session.create()
        authKey = request.session.session_key

    create_or_update_tokens(
        session_id=authKey,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type,
    )

    #create redirect url to song details
    redirect_url = f"http://127.0.0.1:8000/spotify/current-song?key={authKey}"
    return HttpResponseRedirect(redirect_url)

# Check user authentication
class CheckAuthentication(APIView):
    def get(self, request, format = None):
        key = self.request.session.session_key
        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key
        
        auth_status = is_spotify_authenticated(key)

        if auth_status:
            # Will be redirected to the credentials of a song
            redirect_url = f"http://127.0.0.1:8000/spotify/current-song?key={key}"
            return HttpResponseRedirect(redirect_url)
        else:
            #Redirect to AuthenticationURL
            redirect_url = "http://127.0.0.1:8000/spotify/auth-url"
            return HttpResponseRedirect(redirect_url)

class CurrentSong(APIView):
    kwarg = "key"
    def get(self, request, format = None):
        key = request.GET.get(self.kwarg)
        token = Token.objects.filter(user = key)
        print(token)

        # Create endpoint
        endpoint = "player/currently-playing"
        response = spotify_requests_execution(key, endpoint)

        if "error" in response or "item" not in response:
            return Response({}, status = status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        progress = response.get('progress')
        is_playing = response.get('is_playing')
        duration = response.get('duration')
        song_id = response.get('song_id')
        title = response.get('title')
        album_cover = response.get('album_cover')

        artist = ""
        for i, artist in enumerate(item.get("artists")):
            if i > 0:
                artist += ", "
            name = artist.get("name")
            artist += name

        song = {
            "id" : song_id,
            "title" : title,
            "artist" : artist,
            "duration" : duration,
            "time" : progress,
            "album_cover" : album_cover,
            "is_playing" : is_playing
        }

        print(song)
        return Response(song, status = status.HTTP_200_OK)