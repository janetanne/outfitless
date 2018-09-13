import os
import server
import unittest
import requests
import glob
import json
import datetime
import pprint
import random

from flask import Flask, redirect, request, \
                  render_template, session, url_for, flash, \
                  send_from_directory, jsonify

from flask_login import LoginManager, login_required, login_user, \
                        logout_user, current_user, UserMixin

# for debug toolbar
from flask_debugtoolbar import DebugToolbarExtension

# for uploads
from werkzeug.utils import secure_filename

#for jinja
from jinja2 import StrictUndefined

# my code
import config
from helper import get_google_auth, get_concepts, \
                   change_piece_to_dict
from model import User, Piece, Outfit, OutfitPiece, \
                  OutfitWear, Category, CategoryPiece, \
                  connect_to_db, db

# for flask oauth
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

# for google oauth
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# for clarifai
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

##################################################################

c_app = ClarifaiApp()

# for Oufitless app
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = os.environ['APP_SECRET_KEY']
if not app.secret_key:
    print("\n\n\n\nSECRET KEY IS NOT THERE.\n\n\n\n")

else:
    print("\n\n\nSECRET KEY LOADED.\n\n\n")

# google oauth for flask login
app.config.from_object(config.config['dev'])
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

# google oauth
CLIENT_SECRETS_FILE = 'google_oauth_client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata',
          'https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile']

# for uploads #

UPLOAD_FOLDER = './test_uploads' 
# TODO: remember to change this at production
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

######################### routes ###################################
@app.route('/')
def shows_homepage():

    return render_template('home.html')

@app.route('/about')
def shows_aboutpage():

    return render_template('about.html')

@app.route('/logout')
@login_required
def logs_out_user():
    logout_user()
    return redirect('/')

@app.route('/login', methods=["GET"])
def login():

    if current_user.is_authenticated:
        return redirect('/login')

    google = get_google_auth()

    auth_url, state = google.authorization_url(config.Auth.AUTH_URI, 
                      access_type='offline')

    session['oauth_state'] = state

    return render_template('login.html', auth_url=auth_url)

@app.route('/authorize')
def authorize_user():
    """For user's initial authorization for app to access Google Photos Library API."""

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
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect('/mycloset')

    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'

    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))

    else:
        # Execution reaches here when user has
        # successfully authenticated our app.

        # this creates an OAuth2Session object
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            

        else:
            flash('This is not a valid file, please use' + 
                    ' .png/.jpg/.jpeg/.tiff files only.')

    flash('Your photos have been uploaded!')
    return redirect('verifycloset')

@app.route('/upload', methods=['GET'])
@login_required
def show_upload_form():
    """Shows upload form for user to upload photos."""

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/verifycloset', methods=['GET'])
@login_required
def show_uploads():

    upload_data = []

    closet_json = process_image()

    for item in closet_json['outputs']:
        item_concepts = get_concepts(item)
        upload_data.append(item_concepts)

    return render_template('verifycloset.html', 
                            upload_data=upload_data)

@app.route('/verifycloset', methods=['POST'])
@login_required
def process_form():

    # gets data from piece form
    user_id = current_user.user_id
    clothing_type = request.form.get("clothing_type")
    img_url = request.form.get("img_url")
    categories = request.form.getlist("category")
    c_id = request.form.get("c_id")
    desc = request.form.get("desc")
    other_desc = request.form.get("other_desc")
    cost = request.form.get("cost")

    if other_desc:
        desc = other_desc
     
    new_piece = Piece(times_worn=0, 
                      desc=desc, 
                      clothing_type=clothing_type,
                      user_id=user_id,
                      img_url=img_url,
                      cost=cost,
                      cost_per_use=cost)

    db.session.add(new_piece)
    db.session.commit()

    for item in categories:
        check_category = Category.query.filter(Category.category==item)
        check_category = check_category.first()

        # creates new category in categories table
        if not check_category:
            check_category = Category(category=item)
            db.session.add(check_category)
            db.session.commit()

        new_category_piece = CategoryPiece(piece_id=new_piece.piece_id,
                                           cat_id=check_category.cat_id)
        db.session.add(new_category_piece)
        db.session.commit()

    print("\nPOST REQUEST IS HAPPENING\n")

    return c_id

@app.route('/mycloset')
@login_required
def see_closet():

    ### be explicit if you use filter. should be filter(Piece.user_id=current_user.user_id)
    all_pieces = Piece.query.filter_by(user_id=current_user.user_id).all()

    print(current_user.user_id)

    print(all_pieces)

    return render_template('mycloset.html', all_pieces=all_pieces)

####### note: add feature that doesn't reuse outfits given a certain time

@app.route('/ootd', methods=['GET'])
@login_required
def see_todays_outfit():

    all_pieces = Piece.query.filter_by(user_id=current_user.user_id).all()

    if not all_pieces:
        return redirect('/mycloset')

    else:

        all_dresses = Piece.query.filter(Piece.clothing_type == "dress", Piece.user_id==current_user.user_id).all()
        all_tops = Piece.query.filter(Piece.clothing_type == "top", Piece.user_id==current_user.user_id).all()
        all_bottoms = Piece.query.filter(Piece.clothing_type == "bottom", Piece.user_id==current_user.user_id).all()
        all_jackets = Piece.query.filter(Piece.clothing_type == "jacket", Piece.user_id==current_user.user_id).all()

        outfit_dict = {}

        piece_1 = random.choice(all_pieces)
        piece_1 = change_piece_to_dict(piece_1)
        outfit_dict['piece_1'] = piece_1

        if piece_1['clothing_type'] == "dress":
            piece_2 = random.choice(all_jackets)
            piece_2 = change_piece_to_dict(piece_2)
            outfit_dict['piece_2'] = piece_2

        elif piece_1['clothing_type'] == "top":
            piece_2 = random.choice(all_bottoms)
            piece_2 = change_piece_to_dict(piece_2)
            outfit_dict['piece_2'] = piece_2
            piece_3 = random.choice(all_jackets)
            piece_3 = change_piece_to_dict(piece_3)
            outfit_dict['piece_3'] = piece_3

        elif piece_1['clothing_type'] == "bottom":
            piece_2 = random.choice(all_tops)
            piece_2 = change_piece_to_dict(piece_2)
            outfit_dict['piece_2'] = piece_2
            piece_3 = random.choice(all_jackets)
            piece_3 = change_piece_to_dict(piece_3)
            outfit_dict['piece_3'] = piece_3
            
        elif piece_1['clothing_type'] == "jacket":
            piece_2 = random.choice(all_tops)
            piece_2 = change_piece_to_dict(piece_2)
            outfit_dict['piece_2'] = piece_2
            piece_3 = random.choice(all_bottoms)
            piece_3 = change_piece_to_dict(piece_3)
            outfit_dict['piece_3'] = piece_3

        return render_template('ootd.html', outfit=outfit_dict)


@app.route('/ootd', methods=['POST'])
@login_required
def process_outfit():

    user_id = current_user.user_id
    piece_1 = request.form.get("piece_1")
    piece_2 = request.form.get("piece_2")
    piece_3 = request.form.get("piece_3")

    if piece_3 == "0":
        outfit_list = [piece_1, piece_2]
    else:
        outfit_list = [piece_1, piece_2, piece_3]

    new_outfit = Outfit(user_id=user_id)
    db.session.add(new_outfit)
    db.session.commit()

    for piece in outfit_list:
        new_outfit_piece = OutfitPiece(outfit_id=new_outfit.outfit_id,
                                       piece_id=piece)
        check_piece = Piece.query.filter(Piece.piece_id==piece).first()
        if check_piece:
            check_piece.times_worn = (check_piece.times_worn + 1) 
            check_piece.cost_per_use = (check_piece.cost / check_piece.times_worn)
        db.session.add(new_outfit_piece)
        db.session.commit()

    new_outfit_wear = OutfitWear(date_worn=datetime.datetime.now(),
                                 outfit_id=new_outfit.outfit_id)

    db.session.add(new_outfit_wear)
    db.session.commit()

    print("\nIT'S HAPPENING!\n")

    return "Noted as worn!"

################ helper function for clarifai ####################

def process_image():
    """Sends image/dataset to Clarifai, returns JSON of Clarifai results for this batch."""
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

    return model.predict(imageList)


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    connect_to_db(app, 'outfitless_db')

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.

    # NOTE: use this to generate ssl cert & key. 
    # http://werkzeug.pocoo.org/docs/0.14/serving/#loading-contexts-by-hand

    app.run('0.0.0.0', ssl_context=('./ssl.cert', './ssl.key'))