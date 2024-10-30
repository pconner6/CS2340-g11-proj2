
from django.urls import path
from .views import auth_views

urlpatterns = [
    path('', auth_views.landing_page, name='landing_page'),
    path('login/', auth_views.spotify_login, name='spotify_login'),
    path('callback/', auth_views.spotify_callback, name='spotify_callback'),
    path('home/', auth_views.home, name='home'),
    path('wrapped/', auth_views.view_wrapped, name='view_wrapped'),
    path('logout/', auth_views.logout_view, name='logout'),
]
