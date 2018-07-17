import os
from flask import Flask

from .model import db


def load_config(app: Flask):
    env = app.config['ENV']
    if env.lower() == 'production':
        config_file = 'production.py'
    else:
        config_file = 'development.py'
    config_path = os.path.join("config", config_file)
    app.config.from_pyfile(config_path, silent=False)


def create_app(module_name: str):
    app = Flask(module_name)
    load_config(app)

    db.init_app(app)

    return app
