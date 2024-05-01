from flask import Blueprint

#blueprint instantiation
product = Blueprint('product',__name__)
from shop.products import routes
