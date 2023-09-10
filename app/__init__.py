from flask import Flask
from .extensions import db, migrate
from .config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    from .db import models
    return app