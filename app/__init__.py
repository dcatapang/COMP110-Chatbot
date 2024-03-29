from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from spacy import load

app = Flask(__name__)

app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

nlp = load("en_core_web_lg")

from app import routes, models