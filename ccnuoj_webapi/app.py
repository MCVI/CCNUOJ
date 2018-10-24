import os

from flask import Flask
from src import database, blueprint
from src import authentication


common_config_file = ["common.py"]
development_config_file = ["development.py"]
production_config_file = ["production.py"]


def load_config_file(app: Flask, filename: str):
    path = os.path.join("config", filename)
    app.config.from_pyfile(path, silent=False)


def load_config(app: Flask):
    env = app.config['ENV']

    available_config_file = common_config_file.copy()
    if env.lower() == 'production':
        available_config_file.extend(production_config_file)
    else:
        available_config_file.extend(development_config_file)

    for f in available_config_file:
        load_config_file(app, f)


app = Flask(__name__)
load_config(app)
database.init_app(app)
app.register_blueprint(blueprint)

authentication.init(app)


if __name__ == '__main__':
    app.run()
