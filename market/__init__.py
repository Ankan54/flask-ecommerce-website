from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = #replace with a secret key, refer readme file to generate one
db= SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= 'login_page'
login_manager.login_message_category= 'info'
login_manager.login_message= 'Please Sign in to continue'
db.create_all()
from market import routes
