import os

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_SECRET']
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/redirect'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0=eydcga!-#_ddl0f$u*=v%cq#%b2j0aasn1rjwreho0f8r&x*'