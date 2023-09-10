import json
import os

with open('app/config.json', 'r') as f:
    config_data = json.load(f)

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # This is to suppress a warning and save system resources

class DevelopmentConfig(Config):
    DEBUG = config_data['development']['DEBUG']
    SQLALCHEMY_DATABASE_URI = config_data['development']['SQLALCHEMY_DATABASE_URI']
    print(SQLALCHEMY_DATABASE_URI)

config_by_name = dict(
    dev=DevelopmentConfig,
)
# Default config
config = config_by_name.get(os.environ.get('FLASK_ENV', 'dev'))