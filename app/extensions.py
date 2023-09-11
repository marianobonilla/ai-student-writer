from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app
from boto3 import client

def s3_client():
    return client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name='us-west-1'
        )

db = SQLAlchemy()
migrate = Migrate()