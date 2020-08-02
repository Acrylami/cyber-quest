from datetime import datetime
from cyber import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer)
    #password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Training(db.Model):
    __tablename__ = 'training'

    training_name = db.Column(db.String(50), nullable=False, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, nullable=False)



class TrainingProgress(db.Model):
    __tablename__ = 'training-progress'
    u_name = db.Column(db.Integer, nullable=False, primary_key=True)
    t_name = db.Column(db.String(50), nullable=False, primary_key=True)
    date_completed = db.Column(db.DateTime, nullable=False)

    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





