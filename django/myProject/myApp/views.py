# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import ContactForm,SearchForm
from django.conf import settings
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from django.views.generic import TemplateView
from .models import SearchBar
import json
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If user is authenticated, log them in
            auth_login(request, user)  # Use the renamed function
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            # If authentication fails, add an error message
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                # Create a new user
                user = User(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=make_password(password)  # Hash the password
                )
                user.save()  # Save the user to the database
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')  # Redirect to login page after successful registration
            except Exception as e:
                messages.error(request, 'Error: ' + str(e))
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')
class HomeView(TemplateView):
    template_name = 'dashboardcopy.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the search form to the context
        context['search'] = SearchForm()  # Instantiate the SearchForm
        return context


'''class HomeView(TemplateView):
    template_name='dashboardcopy.html'
    search=SearchForm()
    def get(self,request,*args,**kwargs):
        context={
            'search':self.search
        }
        return render(request, 'dashboardcopy.html')'''
def settings_page(request):
    return render(request, 'settings_page.html')
def manage_playlist(request):
    return render(request, 'manage_playlist.html')
def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    return render(request, 'profile.html')
def signout(request):
    return render(request, 'signout.html')

def helpcenter(request):
    return render(request, 'helpcenter.html')
def subscription(request):
    return render(request, 'subscription.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def success(request):
    return render(request, 'success.html')
    
def submit_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # For example, send an email or save to the database
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
import secrets

def spotify_login(request):
    print(f"Type of settings: {type(settings)}")  # This should print <class 'django.conf.LazySettings'>
    print(f"Available settings: {dir(settings)}")  # This will list all attributes in settings

    client_id = settings.SPOTIFY_CLIENT_ID
    redirect_uri = settings.SPOTIFY_REDIRECT_URI
    scope = "user-read-private user-read-email"
    spotify_url = (
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )
    return redirect(spotify_url)

from django.shortcuts import redirect

def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        messages.error(request, "Authorization failed. No code provided.")
        return redirect('home')  # Redirect to home or an error page

    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    redirect_uri = settings.SPOTIFY_REDIRECT_URI

    # Exchange code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # Make the POST request to get the access token
    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        messages.error(request, "Failed to retrieve access token.")
        return redirect('home')  # Redirect to home or an error page

    token_data = response.json()

    # Access the token (save it for further API calls)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    if not access_token:
        messages.error(request, "Access token not found.")
        return redirect('home')  # Redirect to home or an error page

    # Optionally, store the tokens in the session or database
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token

    # Use the access token to fetch Spotify data
    headers = {"Authorization": f"Bearer {access_token}"}
    user_profile_url = "https://api.spotify.com/v1/me"
    user_profile_response = requests.get(user_profile_url, headers=headers)

    if user_profile_response.status_code != 200:
        messages.error(request, "Failed to retrieve user profile.")
        return redirect('home')  # Redirect to home or an error page

    user_data = user_profile_response.json()

    # Render the user data in the template
    return render(request, "spotify_dashboard.html", {"user_data": user_data})


def spotify_dashboard(request):
    return render(request, 'spotify_dashboard.html')
# music/views.py
Client_id =  '9f41210951da421b95be3eef753385a6'
Client_secret = '23df302a7cb94c39a3215cd09b47069b'
def idGenerator(search):
    client_credientials_manager=SpotifyClientCredentials(client_id=Client_id,client_secret=Client_secret)
    sp=spotipy.spotify(client_credientials_manager=client_credientials_manager)
    names=search
    result=sp.search(names)
    if result['tracks']['items'][0]['artists'][0]['name']=='names':
        id=result['tracks']['items'][0]['artists'][0]['id']
        type=result['tracks']['items'][0]['artists'][0]['id']
        return type,id
    elif result['tracks']['items'][0]['type']=='albums':
        id=result['tracks']['items'][0]['id']
        type=result['tracks']['items'][0]['type']
        return type,id
    elif result['tracks']['items'][0]['type']=='track':
       id=result['tracks']['items'][0]['artists'][0]['id']
       type=result['tracks']['items'][0]['artists'][0]['type']
       return type,id
    else:
        id="NOT"
        type="found"
        return type,id
'''def searchbar(request):
    search_query=SearchForm(request.Post or None)
    if request.method == 'POST':
        search_result=search_query.save(commit=False)
        search_result.save()
        key,value=idGenerator(search_result.search)
        if key=="NOT":
             return
        context={
            'key':key,
            'value':value
        }
    return render(request,"search.html",context)
 # Import your idGenerator function if it's in a separate module'''

'''def searchbar(request):
    # Initialize the search form
    search_query = SearchForm(request.POST or None)  # Corrected to request.POST

    context = {}  # Initialize context

    if request.method == 'POST' and search_query.is_valid():  # Check if the form is valid
        # Get the search term from the form
        search_result = search_query.save(commit=False)  # Assuming you want to save the form data
        search_result.save()  # Save the search result

        # Generate the key and value using your idGenerator function
        key, value = idGenerator(search_result.search)  # Assuming search_result has a 'search' attribute

        if key == "NOT":
            # Handle the case where the key is "NOT"
            context['message'] = "No results found."  # Example message
            return render(request, "search.html", context)  # Render the template with the message

        # Add the key and value to the context
        context['key'] = key
        context['value'] = value

    return render(request, "search.html", context) '''
'''def searchbar(request):
    search_query = SearchForm(request.POST or None)
    context = {}

    if request.method == 'POST' and search_query.is_valid():
        search_result = search_query.save(commit=False)
        search_result.save()
        key, value = idGenerator(search_result.search)

        if key == "NOT":
            context['message'] = "No results found."
            return render(request, "search.html", context)

        context['key'] = key
        context['value'] = value

    return render(request, "search.html", context)'''
'''def searchbar(request):
    search_query = SearchForm(request.POST or None)
    context = {}

    if request.method == 'POST' and search_query.is_valid():
        search_result = search_query.save(commit=False)
        search_result.save()
        key, value = idGenerator(search_result.search)  # Ensure this function returns valid identifiers

        # Debugging output
        print(f"Key: {key}, Value: {value}")  # Check what values are being generated

        if key == "NOT":
            context['message'] = "No results found."
        else:
            context['key'] =key  
            context['value'] =value

    return render(request, "search.html", context)
'''
# views.py
from django.shortcuts import render
from .forms import SearchForm
from .utils import idGenerator  # Import the idGenerator function

def search(request):
    search_query = SearchForm(request.POST or None)
    context = {}

    if request.method == 'POST' and search_query.is_valid():
        search_term = search_query.cleaned_data['search']
        key, value = idGenerator(search_term)

        if key == "NOT":
            context['message'] = "No results found."
        else:
            context['key'] = key
            context['value'] = value

    context['search'] = search_query  # Include the search form in the context
    return render(request, "dashboard.html", context)
from .models import Notification

def notifications_list(request):
    # Retrieve notifications for the logged-in user
    notifications = Notification.objects.filter(user_email=request.user.email).order_by('-created_at')
    return render(request, 'myApp/notifications_list.html', {'notifications': notifications})
from django.http import JsonResponse

'''def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user_email=request.user.email)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found.'})
credentials = SpotifyClientCredentials(client_id=Client_id, client_secret=Client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)
@csrf_exempt
def search_song(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')

        # Call Spotify API to search for the song
        headers = {
            'Authorization': 'Bearer YOUR_SPOTIFY_ACCESS_TOKEN',
        }
        response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track', headers=headers)
        songs = response.json()

        # Process the response and return relevant data
        return JsonResponse(songs)'''
def notifications(request):
    return render(request, 'notifications.html')