from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)


app.config.from_object('config')
app.config.from_pyfile('config.py')

#Secret key and database login stored in instance

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from cyber import routes
