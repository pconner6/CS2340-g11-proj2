
from django.urls import path
from .views import auth_views

urlpatterns = [
    path('', auth_views.landing_page, name='landing_page'),  # Landing page
    path('login/', auth_views.spotify_login, name='spotify_login'),  # Spotify login
    path('callback/', auth_views.spotify_callback, name='spotify_callback'),  # Spotify callback
]
