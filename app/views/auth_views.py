import requests
from django.shortcuts import render, redirect
from django.conf import settings

# Landing Page
def landing_page(request):
    return render(request, 'app/landing.html')  # A template called landing.html

# Spotify Login
def spotify_login(request):
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        f"&client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
        "&scope=user-top-read"
    )
    return redirect(auth_url)
def spotify_callback(request):
    code = request.GET.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    if access_token:
        request.session['spotify_token'] = access_token
        # Here, optionally store the Spotify user ID or username if available
        # request.session['spotify_user_id'] = <Spotify User ID from API>

    # Redirect or render a new page after the callback
    return render(request, 'app/callback.html', {'access_token': access_token})
