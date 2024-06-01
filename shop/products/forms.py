from wtforms import IntegerField,FloatField,StringField,TextAreaField,validators,SubmitField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired, Length, Email,EqualTo,NumberRange,InputRequired
from flask_wtf import FlaskForm

class AddproductsForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    submit = SubmitField('Add')


    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_3 = FileField('Image 3', validators=[ FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])


class AddbrandForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()],render_kw={'style': 'width: 128ch'})
    submit = SubmitField('Submit',render_kw={'style': 'width: 56ch'})

class AddCategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()],render_kw={'style': 'width: 128ch'})
    submit = SubmitField('Submit',render_kw={'style': 'width: 56ch'})