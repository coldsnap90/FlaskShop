from shop.extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return RegisteredUser.query.get(user_id)

class RegisteredUser(db.Model, UserMixin):
    __tablename__ = 'registeredusers'
    id = db.Column(db.Integer, primary_key= True)
    firstname = db.Column(db.String(50), unique= False)
    lastname = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    province = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    postalcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(128), unique=False, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self,firstname,lastname,username,email,password,country,province,
                 city,contact,address,postalcode):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.country = country
        self.province = province
        self.city = city
        self.contact = contact
        self.address = address
        self.postalcode = postalcode
      
     

    def __repr__(self):
        return f'''Registered-User({self.firstname},{self.lastname},{self.username},{self.email},{self.password},{self.country},{self.province},
                 {self.city}.{self.contact},{self.address},{self.postalcode},{self.date_created})'''


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return f"Customer-Order({self.invoice},{self.status},{self.customer_id},{self.date_created},{self.orders})"
