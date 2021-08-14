import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    configure(app, test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello! Welcome to OpenEuler FAQ!'

    db.init_app(app)

    from . import review
    app.register_blueprint(review.bp)

    return app


def configure(app, test_config):
    import configparser
    config = configparser.ConfigParser()
    config.read('faq_secret.ini')

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='mysql://'
                                + config['mysql']['username'] + ':'
                                + config['mysql']['password'] + '@'
                                + config['mysql']['ip'] + ':'
                                + config['mysql']['port'] + '/openeuler_faq'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

