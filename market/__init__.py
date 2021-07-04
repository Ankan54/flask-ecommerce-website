import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('sqlite:///market.db')
app.config['SECRET_KEY'] = os.environ.get('7c8154da4c30935e05f8b419')
db= SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= 'login_page'
login_manager.login_message_category= 'info'
login_manager.login_message= 'Please Sign in to continue'
@app.before_first_request
def create_tables():
    db.create_all()
from market import routes
