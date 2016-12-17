# coding: utf-8
import os
from flask import Flask
from flask_moment import Moment
from flask_login import LoginManager

moment = Moment()
login_manager = LoginManager()


def create_app(config_name):
    os.environ['APP_CONFIG_FILE'] = os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.pardir, 'config',
            '{0}.py'.format(config_name)))

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('APP_CONFIG_FILE')

    moment.init_app(app)
    login_manager.init_app(app)

    from .views.main import main
    app.register_blueprint(main)

    from .views.errors import errors
    app.register_blueprint(errors)

    return app
