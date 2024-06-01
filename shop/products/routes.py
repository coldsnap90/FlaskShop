from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import db,photos
from shop.products import product
from shop.auth.models import User
from shop.extensions import bcrypt,db,mail,cache
from .models import Category,Brand,Addproduct
from .forms import AddproductsForm,AddbrandForm,AddCategoryForm
from flask_login import login_required, current_user, logout_user, login_user
import secrets
import os


def brands():

    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def users():
    user = User.get_id(current_user)
    return user

def categories():

    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@product.route('/')
@login_required
def home():

    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products,brands=brands(),categories=categories())


@product.route('/result')
@login_required
def result():

    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/searchresult.html',products=products,brands=brands(),categories=categories())


@product.route('/product/<int:id>')
@login_required
def single_page(id):

    product = get_cached_product(id)
    return render_template('products/single.html',product=product,brands=brands(),categories=categories())


@product.route('/brand/<int:id>')
@login_required
def get_brand(id):

    page = request.args.get('page',1, type=int)
    get_brand = get_cached_brand(id)
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories(),get_brand=get_brand)


@product.route('/categories/<int:id>')
@login_required
def get_category(id):

    page = request.args.get('page',1, type=int)
    get_cat = get_cached_category(id)
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat)


@product.route('/addbrand',methods=['GET','POST'])
@login_required
def add_brand():

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    form = AddbrandForm()

    if form.is_submitted():
        brand = Brand(name=form.brand.data)
        db.session.add(brand)
        flash(f'The brand {brand.name} was added to your database','success')
        db.session.commit()
        return redirect(url_for('product.add_brand'))
    
    if form.errors:
        print('error : ',form.errors)
    return render_template('products/newbrand.html',brands=brands,form=form)

@product.route('/updatebrand/<int:id>',methods=['GET','POST'])
@login_required
def update_brand(id):

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('auth.login'))
    

    updatebrand = get_cached_brand(id)
    brand = request.form.get('brand')

    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('auth.brands'))
    
    brand = updatebrand.name
    return render_template('products/newbrand.html', title='Update brand',brands='brands',updatebrand=updatebrand)


@product.route('/deletebrand/<int:id>', methods=['GET','POST'])
@login_required
def delete_brand(id):

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    brand = get_cached_brand(id)

    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('auth.admin'))
    
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('auth.admin'))


@product.route('/addcategory',methods=['GET','POST'])
@login_required
def add_category():

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    form = AddCategoryForm()

    if form.validate_on_submit():
        category = Category(name=form.category.data)
        db.session.add(category)
        flash(f'The brand {category.name} was added to your database','success')
        db.session.commit()
        return redirect(url_for('product.add_category'))
 
    return render_template('products/newbrand.html',form=form)


@product.route('/updatecategory/<int:id>',methods=['GET','POST'])
@login_required
def update_category(id):

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    form = AddCategoryForm()

    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    
    updatecat = get_cached_category(id)
    category = request.form.get('category')  

    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('auth.categories'))
    
    category = updatecat.name
    return render_template('products/newbrand.html',form=form,updatecat=updatecat)



@product.route('/deletecategory/<int:id>', methods=['GET','POST'])
@login_required
def delete_category(id):

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    category = get_cached_category(id)

    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('auth.admin'))
    
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('auth.admin'))


@product.route('/addproduct', methods=['GET','POST'])
def add_product():
    try:
        admin = User.query.filter_by(id=User.get_id(current_user)).first()
        print(admin)
        if admin.is_admin == False:
            return redirect(url_for('auth.login'))
    except:
        print('fail')

    form = AddproductsForm()
    brands = Brand.query.all()
    categories = Category.query.all()

    if form.is_submitted() and 'image_1' in request.files or form.is_submitted() and form.image_1.data =='test':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        if form.image_1.data != 'test':
            image_1 = photos.save(form.image_1.data)

        else:
            image_1 ='test'

        if form.image_2.data:
            image_2 = photos.save(form.image_2.data)
        
        else:
            image_2=''
       
        if form.image_3.data:
            image_3 = photos.save(form.image_3.data)
        
        else:
            image_3 = ''

        addproduct = Addproduct(name=form.name.data,price=form.price.data,discount=form.discount.data,stock=form.stock.data,colors=form.colors.data,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('auth.admin'))

    return render_template('products/newproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)



@product.route('/updateproduct/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):

    admin = User.query.filter_by(id=User.get_id(current_user)).first()
    print(admin)
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    form = AddproductsForm()
    product = get_cached_product(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.description.data
        product.category_id = category
        product.brand_id = brand

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('auth.admin'))
    
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/newproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)


@product.route('/deleteproduct/<int:id>', methods=['POST'])
@login_required
def delete_product(id):

    admin = users()
    if admin.is_admin == False:
        return redirect(url_for('auth.login'))

    product = Addproduct.query.get_or_404(id)
    product = get_cached_product(id)

    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('auth.admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('auth.admin'))



@cache.cached(timeout = 50,key_prefix='get_cached_brand')
def get_cached_brand(brand_id):

    brand = cache.get(brand_id)

    if brand:
        return brand
    
    else:
        brand = Brand.query.get_or_404(brand_id)
        cache.set(brand_id, brand)
        return brand

@cache.cached(timeout = 50,key_prefix='get_cached_product')
def get_cached_product(product_id):

    product = cache.get(product_id)

    if product:
        return product
    
    else:
        product = Addproduct.query.get_or_404(product_id)
        cache.set(product_id, product)
        return product

@cache.cached(timeout = 50,key_prefix='get_cached_category')
def get_cached_category(cat_id):

    category = cache.get(cat_id)

    if category:
        return category
    
    else:
        category = Category.query.get_or_404(cat_id)
        cache.set(cat_id, category)
        return category