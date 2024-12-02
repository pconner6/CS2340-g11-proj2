
from django.urls import path
from .views import auth_views

urlpatterns = [
    path('', auth_views.landing_page, name='landing_page'),
    path('login/', auth_views.spotify_login, name='spotify_login'),
    path('callback/', auth_views.spotify_callback, name='spotify_callback'),
    path('home/', auth_views.home, name='home'),
    path('wrapped/', auth_views.view_wrapped, name='view_wrapped'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('devs/', auth_views.devs, name='devs'),
    path('holiday-wrapped/', auth_views.holiday_wrapped, name='holiday_wrapped'),
    path('slides/', auth_views.slides, name='slides'),
    path('register/', auth_views.register_view, name='register'),
    path('user-login/', auth_views.login_view, name='user_login'),
    path('manage_wrapped/', auth_views.manage_wrapped, name='manage_wrapped'),
    path('delete_account/', auth_views.delete_account, name='delete_account'),
    path('post-wrapped/', auth_views.post_wrapped, name='post_wrapped'),
    path('public-wrapped/', auth_views.view_public_wrapped, name='view_public_wrapped'),
    path('like-wrapped/', auth_views.like_wrapped, name='like_wrapped'),
]
