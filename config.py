from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
ROOT_URL = environ.get('ROOT_URL')
ADMIN_PASS = environ.get('ADMIN_PASS')