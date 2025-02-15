import requests
import urllib.parse
import time
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
import serial
######################################################
#MUST BE ASSIGNED
port = 'COM4'
######################################################
app  = Flask(__name__)
app.secret_key = '53d355f8-571a-4590-1310-1f9579440851'

CLIENT_ID = '20f39a8c91074af08260ad80370eff2d'
CLIENT_SECRET = 'fe6bb85aa9d84efcb1970592ffbc69ea'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

previousMessege = ""

@app.route('/')
def index():
    return "welcome! <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-read-playback-state'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/return-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }


    #setup serial monitor

    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    while(True):
        time.sleep(3)
        response = requests.get(API_BASE_URL + 'me/player', headers=headers)

        if response.status_code == 302:
            return redirect('/login')
        if response.status_code < 204:
            message = 'Nothing Being-Played'
        playlists = response.json()
        message = playlists['item']['name'] + '-' + playlists['item']['artists'][0]['name']

        print()
        print(message)
        print()
        if(previousMessege != message):
            ser.write(message.encode('utf-8'))

    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        new_token_info['expires_in']
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
