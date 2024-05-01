from flask import Flask
from .config import Config
from .extensions import db,bcrypt,mail,moment,migrate,admin,login_manager,csrf,cache,photos,search
from flask_uploads import configure_uploads
import os




ENV = ''
def create_app(config_class=Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir,"static/images")
    with app.app_context():
        csrf.init_app(app)
        db.init_app(app)
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        bcrypt.init_app(app)
        mail.init_app(app)
        moment.init_app(app)
        admin.init_app(app)
        migrate.init_app(app,db, render_as_batch=True)
        search.init_app(app)
        cache.init_app(app)
        configure_uploads(app, photos)
 
        
        
        from shop.auth import auth as auth_blueprint
        from shop.main import main as main_blueprint
        from shop.products import product as product_blueprint
        from shop.cart import cart as cart_blueprint

    
        app.register_blueprint(auth_blueprint,url_prefix='/auth',templates_folder='templates')
        app.register_blueprint(main_blueprint,url_prefix='/',templates_folder='templates')
        app.register_blueprint(product_blueprint,url_prefix='/product',templates_folder='templates')
        app.register_blueprint(cart_blueprint,url_prefix='/cart',templates_folder='templates')

        cache.clear()
        db.create_all()
    
   

    return app