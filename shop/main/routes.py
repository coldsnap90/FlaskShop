from shop.extensions import bcrypt,db,mail,cache
from shop.main import main
from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginForm, testForm
from .models import RegisteredUser,CustomerOrder
import stripe
import secrets
import pdfkit # type: ignore
from shop.products.routes import brands, categories
from flask_wtf.csrf import CSRFError

@main.errorhandler(CSRFError)
def handle_csrf_error(e):
    print('CSRF ERROR',e)
    return render_template('csrf_error.html', reason=e.description), 400


stripe.api_key ='sk_test_51LkJFTH3k8WZ4arf1cn55YJ09jFIO9KcdJN0MUjPLuPf6VZQAWTCH2acdjeBqd0DvSaoQFnJaEIs2Z6cfOeCWzoe00d4geyCBm'

@main.route('/payment',methods=['POST'])
@login_required
def payment():

    invoice = request.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Myshop',
      amount=amount,
      currency='cad',
    )
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('main.thanks'))

@main.route('/thanks')
@login_required
def thanks():

    return render_template('customers/thankyou.html')


@main.route('/register', methods=['GET','POST'])
def customer_register():

    form = CustomerRegisterForm()

    if form.is_submitted():
        user = RegisteredUser(firstname= form.firstname.data,lastname = form.lastname.data,username=form.username.data, email=form.email.data,
                        password=form.password.data ,country = form.country.data,province=form.province.data,
                    city=form.city.data,contact=form.contact.data,address=form.address.data,postalcode=form.postalcode.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    
    return render_template('customers/signup.html', form=form)



@main.route('/login', methods=['GET','POST'])
def customer_login():

    form = CustomerLoginForm()
    user = RegisteredUser.query.all()
    if form.validate_on_submit():
        user = RegisteredUser.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('product.home'))
        
        flash('Incorrect email and password','danger')
        return redirect(url_for('main.customer_login'))
            
    return render_template('customers/login.html', form=form)


@main.route('/logout')
@login_required
def customer_logout():

    logout_user()
    return redirect(url_for('main.customer_login'))

def update_shopping_cart():

    for key, shopping in session['shopcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return update_shopping_cart

@main.route('/getorder')
@login_required
def get_order():

    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:       
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['shopcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('shopcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('main.orders',invoice=invoice))
        
        except Exception as e:
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('cart.get_cart'))
    else:
        return redirect(url_for('product.home'))
        


@main.route('/orders/<invoice>')
@login_required
def orders(invoice):

    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = RegisteredUser.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('main.customer_login'))
    
    return render_template('customers/order.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,
                           customer=customer,orders=orders,brands=brands(),categories=categories())




@main.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):

    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id

        if request.method =="POST":
            customer = RegisteredUser.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered =  render_template('customers/pdf.html', invoice=invoice, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
            path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
            pdf = pdfkit.from_string(rendered, False,configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = '@application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
        
    return request(url_for('main.orders'))