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
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'


mail = Mail(app)

from app.users.views import users
from app.main.views import main
from app.posts.views import posts

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)