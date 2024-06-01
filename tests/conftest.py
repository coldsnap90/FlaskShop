import pytest
from shop import create_app,db
from flask_login import login_user
from shop.auth.models import User
from shop.main.models import RegisteredUser
from shop import bcrypt




@pytest.fixture()
def app():
    print('app called')
    app = create_app()
    with app.test_request_context():
        
        db.create_all()
        if User.query.filter_by(email='testuser@gmail.com').first() == None:

            hash_password = bcrypt.generate_password_hash('123456').decode('utf-8')
            user = User(firstname='testfname',lastname='testlastname',username='testuser', email='testuser@gmail.com',
                            password= hash_password,is_admin=True)
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)
            hash_password = bcrypt.generate_password_hash('123456').decode('utf-8')
            user1 = RegisteredUser(firstname= 'c',lastname = 'f',username='cuser', email='cfarb@gmail.com',
                            password=hash_password ,country = 'can',province='bc',
                        city='lang',contact='6046141899',address='string',postalcode='v1m2k7')
            db.session.add(user1)
            db.session.commit()
       
        
    yield app


@pytest.fixture()
def client(app):
    print('client called')
  
    return app.test_client()