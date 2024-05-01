from flask import Blueprint

#blueprint instantiation
auth = Blueprint('auth',__name__)
from shop.auth import routes
