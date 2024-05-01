from flask import Blueprint

#blueprint instantiation
cart = Blueprint('cart',__name__)
from shop.cart import routes
