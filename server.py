from flask import Flask, redirect, request, render_template, session, url_for, flash, send_from_directory, jsonify
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os
import server
import unittest
import requests
import glob
from helper import get_google_auth, get_concepts, process_image
import config

import requests_oauthlib

# from urllib import HTTPError

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
c_app = ClarifaiApp()

from model import User, Closet, Piece, Outfit, OutfitPiece, OutfitWear, connect_to_db, db

# for Oufitless app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = os.environ['APP_SECRET_KEY']

# google oauth for flask login
app.config.from_object(config.config['dev'])
login_manager = LoginManager(app)
# login_manager.login_view = "login"
login_manager.session_protection = "strong"

# google oauth
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
CLIENT_SECRETS_FILE = 'google_oauth_client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata',
          'https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile']

# for uploads in Outfitless app
UPLOAD_FOLDER = './test_uploads' # TODO: remember to change this at production
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
#  @flask_login.login_required
def shows_homepage():

    return render_template('home.html')

@app.route('/login')
def login():

    if current_user.is_authenticated:
        return redirect('/mycloset')

    google = get_google_auth()

    auth_url, state = google.authorization_url(config.Auth.AUTH_URI, 
                      access_type='offline')

    session['oauth_state'] = state

    return render_template('login.html', auth_url=auth_url)

@app.route('/authorize')
def authorize_user():
    """For authorizing user to use Google Photos Library API."""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        print("\n\n\nTHIS WORKED\n\n\n")
        return redirect(url_for('shows_homepage'))

    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'

    if 'code' not in request.args and 'state' not in request.args:
        print("\n\n\n\n3rd if, means code and state not in request\n\n\n")
        return redirect(url_for('login'))

    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])

        try:
            token = google.fetch_token(config.Auth.TOKEN_URI,
                    client_secret=config.Auth.CLIENT_SECRET,
                    authorization_response=request.url)

        except HTTPError: #used to be HTTPError
            return 'HTTPError occurred.'

        google = get_google_auth(token=token)

        resp = google.get(config.Auth.USER_INFO)

        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            
            if user is None:
                user = User()
                user.email = email

            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect(url_for('see_closet'))
        
        return 'Could not fetch your information.'

# for uploads in Outfitless #

def allowed_file(filename):

    # TODO: this only checks the file extension, not the actual type of file
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():

    # check if the post request has the file part
    if 'images' not in request.files:
        flash('You forgot to attach a file, try again.')
        return redirect(request.url)

    file = request.files.getlist('images')

    for f in file:
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Your photo has been uploaded!')

        else:
            flash('This is not a valid file, please use' + 
                    ' .png/.jpg/.jpeg/.tiff files only.')

    return render_template('upload.html')

@app.route('/upload', methods=['GET'])
def show_upload_form():
    """Shows upload form for user to upload photos."""

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# for batch uploads to Clarifai #

# @app.route('/verifycloset')
# def show_closet():

#     closet_json = helper.process_image()

#     for item in closet_json['outputs']:
#         get_concepts(item)

@app.route('/mycloset')
@login_required
def see_closet():

    return render_template('yourcloset.html')

# from werkzeug.serving import make_ssl_devcert
# make_ssl_devcert('./ssl', host='localhost')

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    connect_to_db(app, 'outfitless_db')

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('0.0.0.0', 5000, debug=True)
    # ssl_context=('./ssl.crt', './ssl.key')