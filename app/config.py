import json
import os

with open('app/config.json', 'r') as f:
    config_data = json.load(f)

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # This is to suppress a warning and save system resources

class DevelopmentConfig(Config):
    DEBUG = config_data['development']['DEBUG']
    SQLALCHEMY_DATABASE_URI = config_data['development']['SQLALCHEMY_DATABASE_URI']
    AWS_ACCESS_KEY_ID = config_data['development']['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = config_data['development']['AWS_SECRET_ACCESS_KEY']

config_by_name = dict(
    dev=DevelopmentConfig,
)
# Default config
config = config_by_name.get(os.environ.get('FLASK_ENV', 'dev'))