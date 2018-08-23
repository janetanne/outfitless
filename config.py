import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    REDIRECT_URI = 'https://localhost:5000/oauth2callback'
    AUTH_URI = os.environ['GOOGLE_AUTH_URI']
    TOKEN_URI = os.environ['GOOGLE_TOKEN_URI']
    USER_INFO = 'https://www.googleapis.com/auth/userinfo.profile'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata',
          'https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile']

class Config:
    APP_NAME = "Outfitless"
    SECRET_KEY = os.environ['APP_SECRET_KEY']

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///' + os.path.join(basedir, "test.db")

class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///' + os.path.join(basedir, "prod.db")

config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}