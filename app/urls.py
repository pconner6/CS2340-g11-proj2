
from django.urls import path
from .views import token_views

# urlpatterns = [
#     path('', auth_views.landing_page, name='landing_page'),  # Landing page
#     path('login/', auth_views.spotify_login, name='spotify_login'),  # Spotify login
#     path('callback/', auth_views.spotify_callback, name='spotify_callback'),  # Spotify callback
# ]

urlpatterns = [
    path("auth-url", token_views.AuthenticationURL.as_view()),
    path("redirect", token_views.spotify_redirect),
    path("check-auth", token_views.CheckAuthentication.as_view()),
    path("current-song", token_views.CurrentSong.as_view()),
]