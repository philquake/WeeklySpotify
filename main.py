import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os 

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdasdafibojwnrefiubwourbg'
TOKEN_INFO = 'token_info'

# The function `configure()` loads the environment variables from a .env file.
def configure():
    load_dotenv()

@app.route('/')
def login():
    configure()
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', external = True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
     
    return ("OAUTH SUCCESS")
    

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
            redirect(url_for('login', external=False))

            now = int(time.time())

            is_expired = token_info('expires_at') - now < 60
            if(is_expired):
                 spotipy_oauth = create_spotify_oauth()
                 token_info = spotipy_oauth.refresh_access_token(token_info['refresh_token'])

def create_spotify_oauth():
    return SpotifyOAuth(client_id = ,
                        client_secret= ,
                        redirect_uri= url_for('redirect_page'), _external = True,
                        scope = 'user-library-read playlist-modify-public playlist-modify-private')

app.run(debug=True)