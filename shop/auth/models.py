from shop.extensions import db,login_manager
from flask_login import UserMixin,current_user
from datetime import datetime




@login_manager.user_loader
def load_user(user_id):
    print('called')
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    print('unauthroized')
    return


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50),unique=False)
    lastname = db.Column(db.String(50),unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100),unique=False)
    is_admin = db.Column(db.Boolean,default=False)
    country = db.Column(db.String(50), unique= False)
    province = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    postalcode = db.Column(db.String(50), unique= False)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.now())
    profile = db.Column(db.String(180), unique=False, default='profile.jpg')

    def __init__(self,firstname,lastname,username,email,password,is_admin,country,province,
                 city,contact,address,postalcode):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.country = country
        self.province = province
        self.city = city
        self.contact = contact
        self.address = address
        self.postalcode = postalcode

    def __repr__(self):
        return f'''User({self.firstname},{self.lastname},{self.username},{self.email},{self.password},{self.is_admin},{self.country},{self.province},
                 {self.city}.{self.contact},{self.address},{self.postalcode},{self.date_created})'''

