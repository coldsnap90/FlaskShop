from shop.extensions import bcrypt,db,mail,cache
from shop.cart import cart
from flask import redirect, render_template, session, url_for, flash, request
from flask_login import login_required, current_user, logout_user, login_user
from shop.products.models import Addproduct
from shop.products.routes import brands, categories




def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    
    return False

@cart.route('/addcart', methods=["POST"])
@login_required
def add_cart():
    
    print('addcart')
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method == "POST" and product_id and quantity:
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
        print('returned')
        return redirect(request.referrer)


@cart.route('/getcart')
@login_required
def get_cart():

    if 'shopcart' not in session:
        return redirect(request.referrer)
    
    total_without_tax = 0
    for key, product in session['shopcart'].items():
        total_without_tax += product['price']*int(product['quantity'])
        print('total ',total_without_tax)
        # total += round((subtotal + tax), 2)  
    return render_template('products/cart.html', title="Your Cart", total_without_tax=total_without_tax, brands=brands(),
                            categories=categories())

@cart.route('/empty')
@login_required
def empty_cart():

    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@cart.route('/updatecart/<int:code>', methods=["POST"])
@login_required
def update_cart(code):

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
@login_required
def delete_item(id):

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
@login_required
def clear_cart():

    try:
        session.pop('shopcart', None)
        return redirect(url_for('product.home'))
    except Exception as e:
        print(e)