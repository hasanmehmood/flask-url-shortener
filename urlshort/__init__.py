import os
from flask import Flask, current_app
from flask_pymongo import PyMongo


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'somethingveryrandom'

    # Connecting with MongoDB
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    mongo = PyMongo(app)
    app.config['db'] = mongo.db

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
