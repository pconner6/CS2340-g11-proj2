import requests
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import Wrapped, User
from ..forms import RegisterForm, LoginForm, WrappedForm
import urllib.parse
from django.http import JsonResponse
import json



# Landing Page
def landing_page(request):
    return render(request, 'app/landing.html')  # A template called landing.html

def slides(request):
    return render(request, 'app/slides.html')

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

    # Step 1: Create the Basic Auth header
    auth_header = base64.b64encode(f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()).decode('utf-8')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}"
    }

    # Step 2: Prepare the form data
    data = {
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    # Step 3: Make the POST request to get the access token
    url = "https://accounts.spotify.com/api/token"
    token_response = requests.post(url, headers=headers, data=data)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    if access_token:
        # Step 2: Fetch user information from Spotify
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_url = "https://api.spotify.com/v1/me"
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        spotify_id = user_info.get('id')
        email = user_info.get('email')
        images = user_info.get('images', [])
        if images:
            avatar_url = images[0]['url']
        else:
            avatar_url = None
            
        
        

        # Step 3: Link Spotify account to a User instance
        user, created = User.get_or_create_by_spotify_id(spotify_id=spotify_id, email=email)
        
        if avatar_url:
            user.avatar_url = avatar_url
            user.save()
            
        login(request, user)  # Log in the user

        # Store the access token in the session for future Spotify API requests
        request.session['spotify_token'] = access_token
        # Optionally store additional user data
        # request.session['spotify_user_id'] = <Spotify User ID from API>

        # Redirect to the home page after successful login
        return redirect('home')  # Redirect to the home page

    return render(request, 'app/callback.html', {'error': 'Failed to authenticate with Spotify.'})


def home(request):
    if 'spotify_token' not in request.session:
        return redirect('spotify_login')

    return render(request, 'app/home.html')

def view_wrapped(request):
    if 'spotify_token' not in request.session:
        return redirect('spotify_login')  # Redirect to login if not authenticated

    access_token = request.session['spotify_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Extract the selected time range from the GET request
    
    time_range = request.GET.get('time_range', 'medium_term').strip()

    # Fetch top tracks
    #time_range={time_range}&
    
    #print (time_range)
    
    #print(top_tracks_response.json())
    
    params = {'limit': 10, 'time_range': time_range}
    top_tracks_url = f"https://api.spotify.com/v1/me/top/tracks?{urllib.parse.urlencode(params)}"
    
    #top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?limit=10&'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)
 

    # Fetch top artists
    top_artists_url = f"https://api.spotify.com/v1/me/top/artists?{urllib.parse.urlencode(params)}"
    top_artists_response = requests.get(top_artists_url, headers=headers)
    print(top_tracks_response.json())
    
    if top_tracks_response.status_code == 200 and top_artists_response.status_code == 200:
        top_tracks = top_tracks_response.json().get('items', [])
        top_artists = top_artists_response.json().get('items', [])
        return render(request, 'app/wrapped.html', {
            'top_tracks': top_tracks,
            'top_artists': top_artists,
            'selected_time_range' : time_range,
        })
    else:
        return render(request, 'app/wrapped.html', {
            'error': top_tracks_response.status_code,
            'error_contents': f"Error fetching top tracks: {top_tracks_response.json()}",
            'selected_time_range' : time_range,
            
        })




def logout_view(request):
    if 'spotify_token' in request.session:
        del request.session['spotify_token']

    return redirect('landing_page')


def devs(request):
    developers = [
        {
            'name': 'Elise Docena',
            'email': 'edocena3@gatech.edu',
            'about' : 'Elise is a second year Computer Science major at Georgia Tech with interests in data science and software engineering.'
        },
        {
            'name': 'Cailee Jackson',
            'email': 'cjacks@gatech.edu',
            'about' : 'Cailee is a third year Business major with a concentration in IT Management at Georgia Tech with interests in data analytics and project management.'
        },
        {
            'name': 'Sarah Kilgore',
            'email': 'skilgore7@gatech.edu',
            'about' : 'Sarah is a fourth year Industrial Engineering major at Georgia Tech with a concentration in Analytics and Data Science. '
        },
        {
            'name': 'Paul Conner',
            'email': 'gt email here',
            'about' : 'Paul is _____'
        },
        {
            'name': 'Faris Fakhouri',
            'email': 'gt email here',
            'about' : 'Faris is _____'
        }
    ]

    return render(request, 'app/devs.html', {'developers': developers})

def holiday_wrapped(request):
    if 'spotify_token' not in request.session:
        return redirect('spotify_login')

    access_token = request.session['spotify_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # long term top tracks
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)

    # top artists for long term
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=10'
    top_artists_response = requests.get(top_artists_url, headers=headers)

    if top_tracks_response.status_code == 200 and top_artists_response.status_code == 200:
        top_tracks = top_tracks_response.json().get('items', [])
        return render(request, 'app/holiday_wrapped.html', {'top_tracks': top_tracks})
    else:
        return render(request, 'app/holiday_wrapped.html', {'error': 'Failed to retrieve data from Spotify.'})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')  # Redirect to landing page after logout

def manage_wrapped(request):
    if not request.user.is_authenticated:
        return redirect('login')

    wrapped_items = request.user.wrapped_items.all()  # Get all Wrapped data for the user
    if request.method == "POST":
        wrapped_id = request.POST.get('delete_id')
        Wrapped.objects.filter(id=wrapped_id, user=request.user).delete()

    return render(request, 'app/manage_wrapped.html', {'wrapped_items': wrapped_items})

def delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
        logout(request)
    return redirect('landing_page')




@login_required
def view_public_wrapped(request):
    
    filter_param = request.GET.get('filter', '').strip()
    if filter_param == 'liked':
        public_wrapped = Wrapped.objects.filter(public=True, likes=request.user).order_by('-created_at')
    else:
        public_wrapped = Wrapped.objects.filter(public=True).order_by('-created_at')
    
    
    # I want the cards to be colorful so I am going to define a list of nice random colors to choose from
    colors = [
        "#f2aab4",  # light pink
        "#eafacf",  # cream 
        "#e6ce9a",  # dark cream
        "#9ae6e6",  # cyan
        "#53b2ed",  # sky blue
        "#b47ff5",  # light purple
        "#b4fabe",  # mint
        "#faa0aa",  # rose
    ]
    
    return render(request, 'app/public_wrapped.html', {'public_wrapped': public_wrapped, 'colors': colors, 'filter':filter_param})


@login_required
def post_wrapped(request):
    if 'spotify_token' not in request.session:
        return redirect('spotify_login')  # Redirect to Spotify login if not authenticated

    access_token = request.session['spotify_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Fetch top tracks and artists (as done in view_wrapped)
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?limit=10'
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists?limit=10'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)
    top_artists_response = requests.get(top_artists_url, headers=headers)

    if top_tracks_response.status_code == 200 and top_artists_response.status_code == 200:
        top_tracks = top_tracks_response.json().get('items', [])
        top_artists = top_artists_response.json().get('items', [])
        
        # Prepare the data to be saved
        wrapped_data = {
            'top_tracks': [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in top_tracks],
            'top_artists': [{'name': artist['name'], 'genres': artist['genres']} for artist in top_artists],
            #'created_at': timezone.now(), Json can't serialize this so it causes problems. Will have to make it into string if necessary.
        }

        if request.method == 'POST':
            form = WrappedForm(request.POST)
            if form.is_valid():
                wrapped = form.save(commit=False)
                wrapped.user = request.user
                wrapped.data = wrapped_data  # Assign the prepared data
                wrapped.save()
                return redirect('view_public_wrapped')  # Redirect to public wraps page
        else:
            form = WrappedForm(initial={'data': wrapped_data})

        return render(request, 'app/post_wrapped.html', {'form': form, 'wrapped_data': wrapped_data})
    else:
        return render(request, 'app/post_wrapped.html', {'error': 'Failed to retrieve data from Spotify.'})
    
    
@login_required
@require_POST
def like_wrapped(request):
    try:
        data = json.loads(request.body)
        wrapped_id = data.get('wrapped_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not wrapped_id:
        return JsonResponse({'error': 'No wrapped_id provided'}, status=400)

    wrapped = get_object_or_404(Wrapped, id=wrapped_id, public=True)
    user = request.user

    if wrapped.likes.filter(id=user.id).exists():
        wrapped.likes.remove(user)
        liked = False
    else:
        wrapped.likes.add(user)
        liked = True

    # Return JSON-serializable data only
    return JsonResponse({
        'liked': liked,
        'like_count': wrapped.like_count
    })






