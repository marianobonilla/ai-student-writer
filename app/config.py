from decouple import config

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('POSTGRESSQL_URL', default='')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # This is to suppress a warning and save system resources

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('POSTGRESSQL_URL_DEV', default='')
    
class ProductionConfig(Config):
    DEBUG = False