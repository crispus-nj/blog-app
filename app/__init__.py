from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate  = Migrate()

# login configurations
login_manger = LoginManager()
login_manger.login_view = 'users.login'
login_manger.login_message_category = 'info'

mail = Mail()

def create_app(config_class=DevConfig):

    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.config['SECRET_KEY'] = 'this'

    db.init_app(app)
    login_manger.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.users.views import users
    from app.main.views import main
    from app.posts.views import posts

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    return app