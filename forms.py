from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import  DataRequired, Email, EqualTo, Length

class BarcodeForm(FlaskForm):
	brand = StringField(label=('Название статьи'), validators=[DataRequired(), Length(max=64)])
	article = IntegerField(label=('Артикль'))
	size = StringField(label=('Название статьи'), validators=[DataRequired(), Length(max=64)])
	weigth = StringField(label=('Название статьи'), validators=[DataRequired(), Length(max=64)])
	barcode = SelectField(choices=[('ean13', 'ean13'), ('code128', 'code128')])
	submit = SubmitField()
