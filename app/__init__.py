from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this'
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
Migrate(app, db)
# login configurations
login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'


mail = Mail(app)

from app import views