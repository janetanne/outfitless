from flask import Flask, redirect, request, render_template, session, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os
import server
import unittest
import requests
import glob

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
c_app = ClarifaiApp()

# for google oauth
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = 'google_oauth_client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'library'
API_VERSION = 'v1'

# for Oufitless app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = os.environ['APP_SECRET_KEY']

# for uploads in Outfitless app
UPLOAD_FOLDER = './test_uploads' # TODO: remember to change this at production
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def shows_homepage():

    return render_template('home.html')

# ALL ROUTES FOR GOOGLE OAUTH BELOW #

@app.route('/authorize')
def authorize_user():
    """For authorizing user to use Google Photos Library API."""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES)

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
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
          CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect('/')

@app.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before '
                + 'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
                  **session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                            params={'token': credentials.token},
                            headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.')

    else:
        return('An error occurred.')

@app.route('/clear')
def clear_credentials():
    
    if 'credentials' in session:
        del session['credentials']
    
    return ('Credentials have been cleared.<br><br>')

def credentials_to_dict(credentials):

    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# END ROUTES FOR GOOGLE OAUTH #

# for uploads in Outfitless #

def allowed_file(filename):

    # TODO: this only checks the file extension, not the actual type of file
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# for batch uploads to Clarifai #

@app.route('/upload.json')
def process_image():
    """Sends image/dataset to Clarifai, returns a json of Clarifai results for this batch."""
    index = 0
    counter = 0
    batch_size = 32
    user_files = glob.glob('./test_uploads/*')

    total_files = len(user_files)

    while (counter < total_files):
        print("Processing batch " + str(index+1))

        imageList = []

        for x in range(counter, counter + batch_size - 1):
            try:
                # import pdb; pdb.set_trace()
                imageList.append(ClImage(filename=user_files[x]))
            except IndexError:
                break

        c_app.inputs.bulk_create_images(imageList)

        model = c_app.models.get('apparel')

        counter = counter + batch_size
        index = index + 1

    return jsonify(model.predict(imageList))


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('0.0.0.0', 5000, debug=True)