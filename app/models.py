from email.policy import default
from app import db, login_manger
from flask_login import UserMixin
from datetime import datetime

@login_manger.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

Comment = db.Table(
    'comments',
     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    # comment = db.Column(db.Text, nullable=False, default=datetime.utcnow)

)
    

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(150))
    post = db.relationship('Post', backref='author', lazy=True)
    # , secondary=Comment
    

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



