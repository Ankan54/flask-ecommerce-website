from market import db, bcrypt, login_manager
from flask_login import UserMixin
import locale

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key= True)
    name= db.Column(db.String(length=30), nullable= False, unique= True)
    price = db.Column(db.Integer(),nullable=False)
    barcode= db.Column(db.String(length=12), nullable=False, unique= True)
    description = db.Column(db.String(length=1024), nullable= False, unique= True)
    owner= db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return self.name

    def buy(self,current_user):
        self.owner= current_user.id
        current_user.change_budget(self.price,'buy')
        db.session.commit()
    
    def sell(self,current_user):
        self.owner= None
        current_user.change_budget(self.price,'sell')
        db.session.commit()


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key= True)
    username= db.Column(db.String(length=30), nullable= False, unique= True)
    email= db.Column(db.String(length=50),nullable=False,unique=True)
    password_hashed= db.Column(db.String(length=60),nullable= False)
    budget= db.Column(db.Integer(), default= 1000)
    items = db.relationship('Item', backref= 'owned_user', lazy= True)

    def __repr__(self):
        return self.username + ':' + self.email 

    @property
    def format_budget(self):
        if len(str(self.budget))>=4:
            locale.setlocale(locale.LC_ALL,'as-IN.utf8')
            return  locale.currency(self.budget,symbol=False,grouping=True)
        else:
            return str(self.budget)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,input_pwd):
        self.password_hashed = bcrypt.generate_password_hash(input_pwd).decode('utf-8')

    def check_password(self,input_pwd):
        return bcrypt.check_password_hash(self.password_hashed, input_pwd)

    def can_purchase(self,item_object):
        return self.budget >= item_object.price
    
    def can_sell(self,item_object):
        return item_object in self.items
    
    def change_budget(self,amount, type):
        if type=='buy':
            self.budget-=amount
        elif type=='sell':
            self.budget+=amount

    def add_money(self,amount):
        self.budget+=amount
        db.session.commit()
