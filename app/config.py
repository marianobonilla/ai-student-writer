import json

with open('app/config.json', 'r') as f:
    config_data = json.load(f)

class Config(object):
    DEBUG = config_data['DEBUG']
    SQLALCHEMY_DATABASE_URI = config_data['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = config_data['SQLALCHEMY_TRACK_MODIFICATIONS']  # This is to suppress a warning and save system resources