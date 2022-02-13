from multiprocessing import Manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'this'
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

# login configurations
login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'
from app import views