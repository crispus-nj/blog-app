from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this'
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from app import views