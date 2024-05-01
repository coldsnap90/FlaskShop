from shop.extensions import bcrypt,db,mail,Message,csrf,cache
from shop.cart import cart
from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories
import json



def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@cart.route('/addcart', methods=["POST"])
def add_cart():
    print('add cart')
    try:
        print('trying')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        print('ID : ',product_id, ' Q : ',quantity)
        product = Addproduct.query.filter_by(id=product_id).first()
        print('request method')
        if request.method == "POST" and product_id and quantity:
            print('dict1')
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            if 'shopcart' in session:
                print(session['shopcart'])
                if product_id in session['shopcart']:
                    for key, item in session['shopcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    print("This product is already in your Cart")
                else:
                    session['shopcart'] = merge_dict(session['shopcart'], DictItems)
            else:
                print('session initialize')
                session['shopcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@cart.route('/getcart')
def get_cart():
    print('getting cart')
    if 'shopcart' not in session:
        print('no session')
        return redirect(request.referrer)
    print('session cart : ',session['shopcart'].items())
    total_without_tax = 0
    for key, product in session['shopcart'].items():
        print(key,product)
        # subtotal = 0
        # subtotal += product['price']*product['quantity']
        # # tax += round(0.06 * subtotal, 0)
        total_without_tax += product['price']*int(product['quantity'])
        print('total ',total_without_tax)
        # total += round((subtotal + tax), 2)  
    return render_template('products/cart.html', title="Your Cart", total_without_tax=total_without_tax, brands=brands(),
                            categories=categories())

@cart.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@cart.route('/updatecart/<int:code>', methods=["POST"])
def update_cart(code):
    print('updating cart')
    if 'shopcart' not in session and len(session['shopcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['shopcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item Updated', 'success')
                    return redirect(url_for('cart.get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart.get_cart'))


@cart.route('/deleteitem/<int:id>')
def delete_item(id):
    print('deleting from cart')
    if 'shopcart' not in session or len(session['shopcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['shopcart'].items():
            if int(key) == id:
                session['shopcart'].pop(key, None)
                return redirect(url_for('cart.get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart.get_cart'))


@cart.route('/clearcart')
def clear_cart():
    try:
        session.pop('shopcart', None)
        return redirect(url_for('product.home'))
    except Exception as e:
        print(e)