import requests
import base64
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import datetime

# Landing Page
def landing_page(request):
    return render(request, 'app/landing.html')  # A template called landing.html

def slides(request):
    if 'spotify_token' not in request.session:
        return redirect('spotify_login')  # Redirect to login if not authenticated

    access_token = request.session['spotify_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Fetch top tracks
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?limit=10'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)

    # Fetch top artists
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists?limit=10'
    top_artists_response = requests.get(top_artists_url, headers=headers)
    
    if top_tracks_response.status_code == 200 and top_artists_response.status_code == 200:
        top_tracks = top_tracks_response.json().get('items', []) #Top Tracks
        top_artists = top_artists_response.json().get('items', []) #Top Artist
        # Popularity score (based on artists)
        average = 0 
        for artists in top_artists:
            average += artists.get('popularity', 0)
        average = average/10
        average_message = ""
        if average > 66:
            average_message = "You must be in on all the trends!"
        elif average <= 66 and average > 33:
            average_message = "Perfectly balanced, as all things should be."
        else:
            average_message = "Secret trendsetter?"
        # Genres (based on artist)
        genre = top_artists[0].get('genres', [])
        
        track = top_tracks[0]
        track_artists = track.get('artists', [])
        images = track.get("album", {}).get("images", [])
        if images:
            image_url = images[0]["url"]  # Return the largest image
        else:
            image_url = None

        return render(request, 'app/slides.html', {
            'top_tracks': top_tracks,
            'top_artists': top_artists,
            'average_popularity': average,
            'average_message': average_message,
            'genres': genre,
            'top_song': track,
            'track_artist': track_artists[0],
            'image_url': image_url


        })
    else:
        return render(request, 'app/slides.html', {
            'error': top_tracks_response.status_code,
        })

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
        request.session['spotify_token'] = access_token
        # Optionally store additional user data
        # request.session['spotify_user_id'] = <Spotify User ID from API>

        # Redirect to the home page after successful login
        return redirect('home')  # Redirect to the home page

    # Handle the case where access token is not received
    return render(request, 'app/callback.html', {'access_token' : access_token})


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

    # Fetch top tracks
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?limit=10'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)

    # Fetch top artists
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists?limit=10'
    top_artists_response = requests.get(top_artists_url, headers=headers)
    
    if top_tracks_response.status_code == 200 and top_artists_response.status_code == 200:
        top_tracks = top_tracks_response.json().get('items', [])
        top_artists = top_artists_response.json().get('items', [])
        return render(request, 'app/wrapped.html', {
            'top_tracks': top_tracks,
            'top_artists': top_artists,
        })
    else:
        return render(request, 'app/wrapped.html', {
            'error': top_tracks_response.status_code,
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
            'email': 'gt email here',
            'about' : 'Sarah is _____'
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
        top_artists = top_artists_response.json().get('items', [])

        holiday_data = {
            'Christmas': [],
            'Halloween': []
        }

        for track in top_tracks:
            track_name = track['name'].lower()
            if "christmas" in track_name or "holiday" in track_name:
                holiday_data['Christmas'].append(track)
            elif "halloween" in track_name or "spooky" in track_name:
                holiday_data['Halloween'].append(track)

        return render(request, 'app/holiday_wrapped.html', {
            'holiday_data': holiday_data,
            'top_artists': top_artists,
        })
    else:
        return render(request, 'app/holiday_wrapped.html', {
            'error': 'Failed to retrieve data from Spotify.',
        })

