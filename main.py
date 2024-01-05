import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
<<<<<<< HEAD

=======
from dotenv import load_dotenv
import os 
>>>>>>> 48ff13ea292384b09cf1ffe1af6f7fb4019dc644
from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
# set a random secret key to sign the cookie
app.secret_key = 'asdasdafibojwnrefiubwourbg'
# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

# loads the environment variables from a .env file.
def configure():
    load_dotenv()

# route to handle logging in
@app.route('/')
def login():
    configure()
     # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

# route to handle the redirect URI after authorizatio
@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', _external = True))

# route to save the Discover Weekly songs to a playlist
@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        # get the token info from the session
        token_info = get_token()
    except:
         # if the token info is not found, redirect the user to the login route
        print("User not logged in")
        return redirect("/")
    
    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # get the user's playlists
    current_playlists = sp.current_user_playlists()['items']
    saved_weekly_playlist_id = None
    discover_weekly_playlist_id = None
    user_id = sp.current_user()['id']

    # find the Discover Weekly and Saved Weekly playlists
    for playlist in current_playlists:
        if(playlist['name'] == 'Discover Weekly'):
            discover_weekly_playlist_id = playlist['id']
        if(playlist['name'] == 'Saved Weekly'):
            saved_weekly_playlist_id = playlist['id']
    
    if not discover_weekly_playlist_id:
         return 'Discover Weekly not found', discover_weekly_playlist_id
    
    if not saved_weekly_playlist_id:
         new_playlist = sp.user_playlist_create(user_id, 'Saved Weekly', True)
         saved_weekly_playlist_id = new_playlist['id']
    
    #retrieve song data from the Discover Weekly Playlist
    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_uris = []
    for song in discover_weekly_playlist['items']:
         song_uri = song['track']['uri']
         song_uris.append(song_uri)

    # add the tracks to the Saved Weekly playlist     
    sp.user_playlist_add_tracks(user_id, saved_weekly_playlist_id, song_uris, None )
    return("Success")         

# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
            redirect(url_for('login', _external=False))

    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
            spotipy_oauth = create_spotify_oauth()
            token_info = spotipy_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect (url_for('login', external=False))

    now = int((time.time))

    is_expired = token_info['expires_at'] - now < 60

    now = int(time.time())

def create_spotify_oauth():
    return SpotifyOAuth(client_id = os.getenv('client_id'),
                        client_secret= os.getenv('client_secret'),
                        redirect_uri= url_for('redirect_page', _external = True),
                        scope = 'user-library-read playlist-modify-public playlist-modify-private')

app.run(debug=True)