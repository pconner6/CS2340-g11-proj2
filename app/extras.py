from .models import Token
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from requests import post, get

BASE_URL = 'https;//api.spotify.com/v1/me'

# 1) Check if tokens exist
def check_tokens(session_id):
    tokens = Token.objects.filter(user = session_id)
    if tokens:
        return tokens[0]
    else:
        return None

# 2) Create and update token model
def create_or_update_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds = expires_in)
    # Update tokens
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = Token(
            user = session_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
            token_type = token_type,
        )
        tokens.save()

# 3) Check authentication
def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)

    if tokens:
        if tokens.expires_in <= timezone.now():
            pass
        return True
    return False

# 4) refresh token function
def refresh_token_func(session_id):
    refresh_token = check_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'client_id' : settings.SPOTIFY_CLIENT_ID,
        'client_secret' : settings.SPOTIFY_CLIENT_SECRET,
    })

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    create_or_update_tokens(
        session_id=session_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type,
    )

def spotify_requests_execution(session_id, endpoint):
    token = check_tokens(session_id)
    headers = {'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + token.access_token}

    # Get data on the song from the spotify API
    response = get(BASE_URL + endpoint, {}, headers = headers)
    if response:
        print(response)
    else:
        print('No Response :(')
    try:
        return response.json()
    except:
        return {'Error' : 'Issue with request'}