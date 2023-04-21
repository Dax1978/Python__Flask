import os

# pip install python-dotenv
# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from blog.enums import EnvType

file_path = os.path.abspath(os.getcwd()) + '/blog/'

load_dotenv()

ENV = os.getenv('FLASK_ENV', default=EnvType.PRODUCTION)
DEBUG = ENV == EnvType.DEVELOPMENT

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path + str(os.getenv('DATABASE_NAME'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True

FLASK_ADMIN_SWATCH = 'pulse'

OPENAPI_URL_PREFIX = '/api/docs'
OPENAPI_VERSION = '3.0.0'
OPENAPI_SWAGGER_UI_PATH = '/'
OPENAPI_SWAGGER_UI_VERSION = '3.51.1'  # see version on https://cdnjs.com/libraries/swagger-ui
