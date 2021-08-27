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
    from faq.setting import DevConfig
    app.config.from_object(DevConfig)

    if test_config is not None:
        # load the tests config if passed in
        app.config.from_mapping(test_config)
