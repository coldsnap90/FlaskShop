from shop.products.routes import brands,categories
from shop.products.models import Addproduct,Brand,Category
from shop.auth.models import User
from shop.main.models import RegisteredUser
from flask import request
import json
import pytest
from pathlib import Path
resources = Path(__file__).parent / "resources"


class authlogin:

    def login(client):
        data = {
                "email": "cfarb@gmail.com", 
                "password": "123456", 
            }
        response = client.post(
                "/login",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
        return response
        
    def adminLogin(client):
        data = {
                "email": "testuser@gmail.com", 
                "password": "123456", 
            }
        response = client.post(
                "/auth/login",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
        return response



@pytest.mark.skip
def test_admin_createLoginPrivelege(client,app):

    print('test admin')
    response = client.get('/auth/login')
    assert response.status_code == 200

    with app.app_context():
        response = authlogin.adminLogin(client)
        assert response.status_code == 302

        response = client.get('/auth/admin')
        assert response.status_code == 200



@pytest.mark.skip
def test_login_route(client,app):

    print('test login')

    with app.app_context():
        response = client.get('/login')
        assert response.status_code == 200
        assert b'<div class="text-center bg-info p-2 h4">Login</div>' in response.data


@pytest.mark.skip
def test_product_route(client,app):

    print('Test product')

    with app.app_context():
        response = client.get('/product/')
        assert response.status_code == 200


@pytest.mark.skip
def test_register_route(app,client):
     
     print('test register')
     
     with app.app_context():
        response = client.get('/register')
        assert response.status_code == 200

        data = {'firstname':'colton','lastname':'castle','username':'cfarbatuk', 'email':'cfarbatuk@gmail.com',
                        'password':'123456' ,'country':'canada','province':'BC',
                        'city':'Abbotsford','contact':'6046141826','address':'33259 rob ave','postalcode':'v2s0l0'
                    }
        response = client.post("/register",
                                    data=json.dumps(data),
                                    headers={"Content-Type": "application/json"},
                                    )
        assert response.status_code == 302
  
        newUser = RegisteredUser.query.filter_by(email='cfarbatuk@gmail.com').first()
        assert str(newUser.firstname) == 'colton'

@pytest.mark.skip
def test_register_login_route(app,client):

    print('test registeredUser login')

    with app.app_context():
        response = client.get('/login')
        assert response.status_code == 200

        data = {
                "email": "cfarb@gmail.com", 
                "password": "123456", 
            }
        response = client.post(
                "/login",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
        assert response.status_code == 302

@pytest.mark.skip
def test_add_category_route(client,app):

    print('test add category')

    with app.app_context():
        response = authlogin.adminLogin(client)
        response = client.get('/product/addcategory')
        assert response.status_code == 200

    
        data = {"category":"electronics"}
        response = client.post(
                    "/product/addcategory",
                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"},
                )
        assert response.status_code == 302  

        cat = Category.query.filter_by(name='electronics').first()
        assert str(cat.name) == "electronics"

@pytest.mark.skip
def test_add_brand_route(client,app):

    print('test add brand')

    with app.app_context():
        response = authlogin.adminLogin(client)
        response = client.get('/product/addbrand')
        assert response.status_code == 200

   
        data = {"brand":"samsung"}
        response = client.post(
                    "/product/addbrand",
                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"},
                )
        assert response.status_code == 302

        bran = Brand.query.filter_by(name='samsung').first()
        assert str(bran.name) == 'samsung'
       

@pytest.mark.skip
def test_addProduct_route(client,app):

    print('test add product')

    with app.app_context():

        response = authlogin.adminLogin(client)
        response = client.get('/product/addproduct')
        assert response.status_code == 200


        data = {"name":"Galaxy 20","price":"159.99","discount":0, "stock":10,
                    "colors":"black" ,"description":"Galaxy phone","image_1":(resources / "960616298f3a979fea1d.jpeg").open("rb"),"image_2":"","image_3":""
                   ,"brand":1,"category":1}
        
        response = client.post(
                    "/product/addproduct",
                    data=data,
                  
                    headers={"Content-Type": "multipart/form-data"},
                )
        assert response.status_code == 302

        bran = Addproduct.query.filter_by(name='Galaxy 20').first()
        assert str(bran.name) =="Galaxy 20"
    
     
@pytest.mark.skip
def test_result_route(client,app):

    print('test result')

    response = client.get('/product/result?q=apple')
    assert response.status_code == 200


@pytest.mark.skip
def test_categories_route(client,app):

    print('test categories')

    response = client.get('/product/categories/1')
    assert response.status_code == 200


@pytest.mark.skip
def test_brand_route(client,app):

    print('test brand route')

    response = client.get('/product/brand/1')
    assert response.status_code == 200

@pytest.mark.skip
def test_thanks_route(client,app):

    print('test thanks route ')

    response = client.get('/thanks')
    assert response.status_code == 200

@pytest.mark.skip
def test_logout_route(client,app):

    print('test logout')

    response = client.get('/logout')
    assert response.status_code == 302
     

def test_addClearCart_route(client,app):

    print('test add-clear cart')

    with app.app_context():
        response = authlogin.login(client)
        response = client.get('/product/')
        assert response.status_code == 200
        
    
        data = {"colors":"black","quantity":"1","product_id":1}
        response = client.post(
                    "/cart/addcart",
                    data=data,
                  
                    headers={"Content-Type": "multipart/form-data"},
                )
        assert response.status_code == 302 

        response = client.get('/cart/getcart')
        assert response.status_code == 200

        response = client.get('/cart/clearcart')
        assert response.status_code == 302
       
        

def test_updateDelete_cart(client,app):
        
        print('test update-delete cart ')

        with app.app_context():
            response = client.get('/product/')
            assert response.status_code == 200
            
        
            data = {"colors":"black","quantity":"1","product_id":1}
            response = client.post(
                        "/cart/addcart",
                        data=data,
                    
                        headers={"Content-Type": "multipart/form-data"},
                    )
            assert response.status_code == 302
            print(response.data)

            response = client.get('/cart/getcart')
            assert response.status_code == 200 and b'<td>Galaxy 20</td>' in response.data
            data = {"color":"black","qauntity":"2"}
            response = client.post(
                        "/cart/updatecart/1",data=data,
                      
                        headers={"Content-Type": "multipart/form-data"},
                    )
            assert response.status_code == 302

            response = client.get(
                        "/cart/deleteitem/1",
                      
                        headers={"Content-Type": "multipart/form-data"},
                    )
            assert response.status_code == 302
      
            
def test_getOrder_route(client,app):

    print('test get order route')

    with app.app_context():
        response = authlogin.login(client)
        response = client.get('/product/')
        assert response.status_code == 200
        
    
        data = {"colors":"black","quantity":"1","product_id":1}
        response = client.post(
                    "/cart/addcart",
                    data=data,
                  
                    headers={"Content-Type": "multipart/form-data"},
                )
        assert response.status_code == 302 

        response = client.get('/getorder')
        assert response.status_code == 302 
       

        



        
    
     