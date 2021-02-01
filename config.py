"""Flask configuration"""
from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    SECRET_KEY = environ.get('SECRET_KEY')

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class ProdConfig(Config):
    DEBUG = False 
    TESTING = False
    FLASK_ENV = 'production'