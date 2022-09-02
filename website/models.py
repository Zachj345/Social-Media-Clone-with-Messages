from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime


'''APP CONFIGURATION'''


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:*****@localhost/social'
app.config['SECRET_KEY'] = '**********'


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.sign_up_login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


'''DATABASES'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(111), nullable=False)
    username = db.Column(db.String(111), nullable=False, unique=True)
    password = db.Column(db.String(111), nullable=False)
    messages = db.relationship('Messages', cascade='all, delete, delete-orphan',
                               backref='user', lazy=True, passive_deletes=True)
    posts = db.relationship('Post', cascade='all, delete, delete-orphan',
                            backref='user', lazy=True, passive_deletes=True)
    comments = db.relationship(
        'Comment', cascade='all, delete, delete-orphan', backref='user', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='user', lazy=True, passive_deletes=True)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    receiver = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255),
                     default=datetime.now().strftime("%m/%d/%Y, %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255),
                     default=datetime.now().strftime("%m/%d/%Y, %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(220), nullable=False)
    time = db.Column(
        db.String(255), default=datetime.now().strftime("%m/%d/%Y, %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship(
        'Comment', backref='post', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='post', lazy=True, passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(380), nullable=False)
    time = db.Column(
        db.String(255), default=datetime.now().strftime("%m/%d/%Y, %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(
        db.String(255), default=datetime.now().strftime("%m/%d/%Y, %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)
