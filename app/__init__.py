# third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# local imports
from config import app_config
from .database import db
# from .api import api
from .voltage_drop.routes import voltage_drop_bp
import os


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    CORS(app)

    from app import models
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()

    # register blueprints
    # app.register_blueprint(api)
    app.register_blueprint(voltage_drop_bp)
    return app
