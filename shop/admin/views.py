from flask import url_for,abort,redirect,flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView,BaseView,expose
from flask_login import current_user


    
class MyHomeView(AdminIndexView):
    def is_accessible(self):
        print('called')

        if current_user.is_anonymous == True:
            print('returning flase')
            return False
        else:
            print('true')
            return True

    
    @expose('/')
    def index(self):
        if self.is_accessible() == True:
            print('is access')
            return self.render('admin/index.html')
        print('redirect')
        return redirect(url_for('auth.login'))


