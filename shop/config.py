import os
from dotenv import load_dotenv
load_dotenv()


class Config:

    env = 'test'
    ADMIN_PASS = os.environ.get('ENV_ADMIN_PASS')
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    SCHEDULER_API_ENABLED = True  

    if env == 'dev':
        ADMIN_PASS = os.environ.get('ADMIN_PASS')
        SQLALCHEMY_DATABASE_URI = os.environ.get('ENV_DATABASE_CONNECT')
        SERVER_NAME = "127.0.0.1:5000"
        
    elif env =='test':
        LOGIN_DISABLED = True
        ADMIN_PASS = os.environ.get('ADMIN_PASS')
        WTF_CSRF_ENABLED = False
        CSRF_ENABLED = False
        SQLALCHEMY_DATABASE_URI = os.environ.get("ENV_LOCAL_DB")
        SERVER_NAME = "127.0.0.1:5000"

    else:
        ADMIN_PASS = os.environ.get('ADMIN_PASS')
        SQLALCHEMY_DATABASE_URI = os.environ.get("ENV_LOCAL_DB")
        SERVER_NAME = "127.0.0.1:5000"

    SECRET_KEY = os.environ.get('ENV_SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    #email sent through on your server, 25 or 465
    MAIL_PORT = os.environ.get("ENV_MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USERNAME = ('Campsite.booking.service@gmail.com')
    MAIL_PASSWORD = os.environ.get("ENV_MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = 'Campsite.booking.service@gmail.com'
    MAIL_MAX_EMAILS = 1
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE='Lax'
    CACHE_TYPE = 'SimpleCache'


 
    #secure cookies
    #SESSION_COOKIE_SECURE=True
    #SESSION_COOKIE_HTTPONLY=True

