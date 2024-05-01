from shop.extensions import db,login_manager
from flask_login import UserMixin,current_user
import json


@login_manager.user_loader
def load_user(user_id):
    print(User.query.get(user_id))
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    print('unauthroized')
    return


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50),unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100),unique=False)
    is_admin = db.Column(db.Boolean,default=False)
    profile = db.Column(db.String(180), unique=False, default='profile.jpg')

    def __init__(self,firstname,username,email,password,is_admin):
        self.firstname = firstname
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f' firstname : {self.firstname}, username : {self.username}, email: {self.email}, admin : {self.is_admin}'
