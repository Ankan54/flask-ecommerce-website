from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, widgets
from wtforms.validators import EqualTo, Length, Email, DataRequired, NumberRange, ValidationError
from market.models import User,Item

class RegisterForm(FlaskForm):

    def validate_username(self,input_user):
        user= User.query.filter_by(username=input_user.data).first()
        if user:
            raise ValidationError('Username already exists!')
    
    def validate_email(self,input_email):
        email= User.query.filter_by(email=input_email.data).first()
        if email:
            raise ValidationError('Email ID already exists! Please use another one')

    username= StringField(label='User Name:',
                         validators=[Length(min=2,max=30,message='Username needs to between 2 and 30 characters'),
                        DataRequired()])
    email= StringField(label='Email id:',
                     validators=[Email(message='Email is not valid'),
                     Length(min=6,max=50,message='Email needs to between 6 and 30 characters'),DataRequired()])
    password= PasswordField(label='Password:',
                     validators=[Length(min=6, message='Password needs to have atleast 6 characters'),
                     DataRequired()])
    conf_password= PasswordField(label= 'Confirm Password:',
                     validators=[EqualTo('password', message='Password doesn\'t match'),DataRequired()])
    register= SubmitField(label='Register')

class LoginForm(FlaskForm):
    username= StringField(label='User name:', validators=[DataRequired()])
    password= PasswordField(label='Password:', validators=[DataRequired()])
    login = SubmitField(label='Sign in')

class ItemForm(FlaskForm):

    def validate_name(self,input_item):
        item= Item.query.filter_by(name=input_item.data).first()
        if item:
            raise ValidationError('Item already exists!')
    
    def validate_barcode(self,input_barcode):
        item= Item.query.filter_by(barcode=input_barcode.data).first()
        if item:
            raise ValidationError('Barcode already exists!')
    
    def validate_description(self,input_desc):
        item= Item.query.filter_by(description=input_desc.data).first()
        if item:
            raise ValidationError('Description already exists!')

    name= StringField(label='Item Name:',validators=[Length(min=2,max=30,
                    message='Item name needs to have between 2 to 30 characters'),
                    DataRequired()])
    price= IntegerField(label='Item Price:',
                        validators=[NumberRange(min=1,message='Price can not be less than 1')],
                        widget=widgets.Input(input_type='number'))
    barcode= StringField(label='Barcode:',
                         validators=[Length(min=12,max=12,message='Barcode needs to be of 12 characters')])
    description= StringField(label='Description',validators=[DataRequired()])
    add_item= SubmitField(label='Add Item')


class PurchaseItemForm(FlaskForm):
    purchase= SubmitField(label='Purchase')
    
class SellItemForm(FlaskForm):
    sell = SubmitField(label='Sell')

class AddMoneyForm(FlaskForm):

    def validate_amount(self,amount):
        if amount.data<=1:
            raise ValidationError('Amount must be greater than 0')
        elif amount.data % 100:
            raise ValidationError('Amount must be mulitple of 100')

    amount= IntegerField(validators=[DataRequired()],
                        widget=widgets.Input(input_type='number'))
    add_money= SubmitField(label='Add Money')
