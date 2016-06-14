import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'change-this'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAPZEN_API_KEY = os.environ['MAPZEN_API_KEY']

    #Specify Location Coordinates for Geocoder
    LOCATION_LAT = '40.730610'
    LOCATION_LONG = '-73.935242'
    LOCATION_RADIUS_KM = '100'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
