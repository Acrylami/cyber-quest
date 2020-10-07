from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)


app.config.from_object('config')
app.config.from_pyfile('config.py')

#app.config['SECRET_KEY'] = '6c56ad55dbd1c8779d65f05b9335ec9d'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1803625:^Q@S(3zhPyq:@csmysql.cs.cf.ac.uk:3306/c1803625'
#SPECIFY YOUR MYSQL CREDIENTIALS:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:MYSQL_PASSWORD@csmysql.cs.cf.ac.uk:3306/USERNAME'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from cyber import routes
