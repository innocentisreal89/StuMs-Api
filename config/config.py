import os
from decouple import config
from datetime import timedelta


base_dir = os.path.dirname(os.path.realpath(__file__))

#This has to do with the Prod. config, it is a replacement for the  'DATABASE_URL'  we had use already
uri =config('DATABASE_URL')
if uri.startswith('posgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1) # to make it compatible wih sql

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Student Management System"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    





#other settings will inherit from the config class above
#to set our develop config
class DevConfig(Config):
    DEBUG = config('DEBUG', True, cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite3')

#to set our test config
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' 
    
#to set our Production config
class ProdConfig():
    SQLALCHEMY_DATABASE_URI = uri               
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)

#this config_dict is created so dat we can easily read/hold these classes
config_dict = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}