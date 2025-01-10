# utils.py
import requests

def idGenerator(search_term):
    CLIENT_ID = '9f41210951da421b95be3eef753385a6'  # Replace with your Spotify client ID
    CLIENT_SECRET = '23df302a7cb94c39a3215cd09b47069b'  # Replace with your Spotify client secret

    # Get an access token
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    # Search for the track
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    search_url = f'https://api.spotify.com/v1/search?q={search_term}&type=track'
    search_response = requests.get(search_url, headers=headers)
    search_results = search_response.json()

    # Check if any tracks were found
    if search_results['tracks']['items']:
        track = search_results['tracks']['items'][0]  # Get the first track
        track_id = track['id']  # Get the track ID
        return 'track', track_id  # Return the type and ID
    else:
        return 'NOT', None  # No valid result found