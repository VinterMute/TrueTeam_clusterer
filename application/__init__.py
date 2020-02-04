from flask import Flask
from config import Config

STATIC_FOLDER = 'templates/'

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.from_object(Config)

from application import routes  # bottom import is necessary to avoid flask cyclic import error
