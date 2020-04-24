from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# # email server
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 25
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
#
# # Set environment variables for authentication
# os.environ['EMAIL_USERNAME'] = '' #input your email address
# os.environ['EMAIL_PASSWORD'] = '' #input your password
#
# # administrator list
# ADMINS = [''] # again input your email address as a sender

from MysterEats_App import routes
