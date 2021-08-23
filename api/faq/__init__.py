import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    configure(app, test_config)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello! Welcome to OpenEuler FAQ!'

    db.init_app(app)

    from faq import blueprints
    app.register_blueprint(blueprints.bp)
    from faq import es_handler
    app.register_blueprint(es_handler.bp)

    return app


def configure(app, test_config):
    import configparser
    config = configparser.ConfigParser()
    config.read('faq_secret.ini')
    assert 'mysql' in config
    assert 'username' in config['mysql']
    assert 'password' in config['mysql']
    assert 'ip' in config['mysql']
    assert 'port' in config['mysql']
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
        # load the tests config if passed in
        app.config.from_mapping(test_config)
