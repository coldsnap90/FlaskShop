from wtforms import StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError, SubmitField
from flask_wtf.file import FileRequired,FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email,EqualTo,NumberRange,InputRequired
from flask_wtf import FlaskForm
from .models import RegisteredUser





class CustomerRegisterForm(FlaskForm):
    firstname = StringField('Name: ')
    username = StringField('Username: ', validators = [DataRequired()])
    email = StringField('Email: ', validators = [Email(), DataRequired()])
    password = PasswordField('Password: ', validators =[DataRequired(), EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', validators =[DataRequired(), EqualTo('confirm', message=' Both password must match! ')])
    country = StringField('Country: ')
    province = StringField('Province: ')
    city = StringField('City: ')
    contact = StringField('Contact: ')
    address = StringField('Address: ')
    postalcode = StringField('Postal code: ')
    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        if RegisteredUser.query.filter_by(username=username).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if RegisteredUser.query.filter_by(email=email).first():
            raise ValidationError("This email address is already in use!")
        

class testForm(FlaskForm):
    test = StringField('Test',validators=[DataRequired()])
    datas = StringField('empty')
    submit = SubmitField('testsub')


class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    submit = SubmitField('Login')

   