from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_moment import Moment
from flask_migrate import Migrate
from flask_caching import Cache
from flask_uploads import UploadSet,IMAGES
from flask_msearch import Search
from flask_wtf import CSRFProtect
from shop.admin.views import MyHomeView




db = SQLAlchemy()
bcrypt = Bcrypt()
moment = Moment()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin(index_view=MyHomeView())
search = Search(db=db)
cache = Cache()
photos = UploadSet('photos', IMAGES)
csrf = CSRFProtect()



