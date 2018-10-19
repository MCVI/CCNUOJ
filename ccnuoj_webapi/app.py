import os

from flask import Flask
from src import database, blueprint
from src import authentication


def load_config(app: Flask):
    env = app.config['ENV']
    if env.lower() == 'production':
        config_file = 'production.py'
    else:
        config_file = 'development.py'
    config_path = os.path.join("config", config_file)
    app.config.from_pyfile(config_path, silent=False)


app = Flask(__name__)
load_config(app)
database.init_app(app)
app.register_blueprint(blueprint)

authentication.init(app)

if __name__ == '__main__':
    app.run()
