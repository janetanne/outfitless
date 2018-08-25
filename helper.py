import requests_oauthlib
from config import Auth, Config, DevConfig, ProdConfig, config
import glob
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

def get_google_auth(state=None, token=None):
    """Helper function to create OAuth2Session object."""

    if token:
        return requests_oauthlib.OAuth2Session(Auth.CLIENT_ID, token=token)

    if state:
        return requests_oauthlib.OAuth2Session(Auth.CLIENT_ID,
                             state=state,
                             redirect_uri=Auth.REDIRECT_URI)

    oauth = requests_oauthlib.OAuth2Session(Auth.CLIENT_ID,
                          redirect_uri=Auth.REDIRECT_URI,
                          scope=Auth.SCOPES)
    return oauth

# to get the first three concepts in the JSON:

def get_concepts(_dict):
    """Takes in dictionary (or JSON) and returns a list with 
    the first three concepts for an item."""
    counter = 0
    piece_data = {}

    piece_data['piece_url'] = _dict['input']['data']['image']['url']
    piece_data['c_id'] = _dict['id']
    piece_data['concepts'] = []

    while counter <= 2:
        concept = _dict['data']['concepts'][counter]['name']
        piece_data['concepts'].append(concept)
        counter +=1

    return piece_data

# for item in batch['outputs']:
#     return("FUNCTION PULLS: {}".format(get_concepts(item))

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

    return jsonify(model.predict(imageList))
