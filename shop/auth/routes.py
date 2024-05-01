from flask import render_template,session, request,redirect,url_for,flash
from shop.extensions import bcrypt,db,mail,Message,csrf,cache,login_manager
from flask_login import login_user, current_user, logout_user, login_required
from shop.auth import auth
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Brand
import time
import psycopg2
import os
from psycopg2.extras import RealDictCursor

def get_db_connect():
    while True:
        try:
            conn = psycopg2.connect(dbname=os.environ.get('DBNAME'), user=os.environ.get('USER'), host=os.environ.get('LOCALHOST'), password=os.environ.get('PASSWORD'), port=os.environ.get('PORT'),cursor_factory = RealDictCursor)
            cur = conn.cursor()
            return conn,cur
        except Exception as error:
            print('Connecting to DB failed')
        time.sleep(2)

@auth.route('/admin')
@login_required
def admin():
    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    if admin.is_admin:
        products = Addproduct.query.all()
        return render_template('admin/index.html', title='Admin page',products=products)

@auth.route('/brands')
@login_required
def brands():
    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    if admin.is_admin:
        brands = Brand.query.order_by(Brand.id.desc()).all()
        return render_template('admin/adminbrand.html', title='brands',brands=brands)


@auth.route('/categories')
@login_required
def categories():
    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    if admin.is_admin:
        categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/adminbrand.html', title='categories',categories=categories)

@auth.route('/data1',methods=['GET', 'POST'])
def data1():
    conn,cur = get_db_connect()
    if 1:
        user1 = User(firstname='Colton',username='cfarbatuk', email='cfarbatuk@gmail.com',
                    password='123456' ,is_admin=True)
        db.session.add(user1)
        db.session.commit()
        return redirect(url_for('auth.data'))
    c = User.query.all()
    return render_template('admin/data.html',c=c)

@auth.route('/data',methods=['GET', 'POST'])
def data():
    c = User.query.all()
    print(c)
    return render_template('admin/data.html',c=c)

@auth.route('/datadel',methods=['GET', 'POST'])
def datadel():
    c = User.query.all()
    for i in c:
        db.session.delete(i)
        db.session.commit()
    return render_template('admin/data.html',c=c)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.data)
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print('hash')
        user = User(firstname=form.firstname.data,username=form.username.data, email=form.email.data,
                    password=hash_password ,is_admin=True)
        db.session.add(user)
        db.session.commit()
        print('first ',User.query.all())
        print('user > ',user)
        flash(f'welcome {form.firstname.data} Thanks for registering','success')

        return redirect(url_for('auth.login'))
    return render_template('admin/adminsignup.html',title='Register user', form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email='cfarbatuk@gmail.com').first()
        print('user ',user)
        if user:
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
            #user.email = form.email.data
            flash(f'welcome {user.email} you are logedin now','success')
            login_user(user,remember=True)
            return redirect(url_for('auth.admin'))
        else:
            
            flash(f'Wrong email and password', 'success')
            return redirect(url_for('auth.login'))
    return render_template('admin/adminlogin.html',title='Login page',form=form)

@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print('admin : ',admin)
    if admin.is_admin:
        logout_user()
    return redirect(url_for('auth.login'))