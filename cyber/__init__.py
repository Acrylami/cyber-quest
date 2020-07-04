from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '6c56ad55dbd1c8779d65f05b9335ec9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1803625:Venrodam123@csmysql.cs.cf.ac.uk:3306/c1803625'
#SPECIFY YOUR MYSQL CREDIENTIALS:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:MYSQL_PASSWORD@csmysql.cs.cf.ac.uk:3306/USERNAME'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from cyber import routes
