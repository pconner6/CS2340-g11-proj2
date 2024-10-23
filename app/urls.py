
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing page
    path('login/', views.spotify_login, name='spotify_login'),  # Spotify login
    path('callback/', views.spotify_callback, name='spotify_callback'),  # Spotify callback
]
