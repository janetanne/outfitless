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


def change_piece_to_dict(item):
    """Takes in list of piece objects and returns a dictionary."""

    piece_dict = {}

    piece_dict['piece_id'] = item.piece_id
    piece_dict['img_url'] = item.img_url
    piece_dict['clothing_type'] = item.clothing_type

    return piece_dict









