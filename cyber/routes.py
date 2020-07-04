import os
from flask import render_template, url_for, request, redirect, flash, session
from cyber import app, db
from cyber.models import *
from cyber.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import *

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',  title='CyberQuest')

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route("/stories")
def stories():
    return render_template('stories.html', title='Choose Your Adventure')

@app.route("/training")
def training():
    return render_template('training.html', title='Training')

@app.route("/viper")
def viper():
    return render_template('viper.html', title='Viper in the Dusk')

#Flask lab 3: implementation of Cart.  Needs 'session' import!
# https://github.com/kkschick/ubermelon-shopping-app/blob/master/melons.py MELONS





