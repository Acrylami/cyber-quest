import os
from flask import render_template, url_for, request, redirect, flash, session
from cyber import app, db
from cyber.models import *
from cyber.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import *
from flask.helpers import flash

@app.route("/")
@app.route("/home")
def home():
    return render_template('stories.html',  title='CyberQuest')

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data, points=0)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created, and you are now logged in!')
        if 'url' in session:
            return redirect(session['url'])
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
            ###
            print(session['url'])
            if 'url' in session:
                return redirect(session['url'])
            return redirect(url_for('home'))
        flash('Invalid username or password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route("/stories")
def stories():
    session['url'] = url_for('stories')   
    return render_template('stories.html', title='Choose Your Adventure')

@app.route("/training")
def training():
    session['url'] = url_for('training')
    #training_entries = Training.query.all()

    #query training progress for this user
    #must check that a user is logged in first
    
    '''
    pull all training entries
    pull training entry for that training name and current user
    if result returned, set completed flag to one
    else set flag to zero
    '''
    crypto = []
    osint = []
    stego = []
    general = []
    web = []
    forensics = []
    
    training_entries = Training.query.all()
    testvar = "hi"
    for entry in training_entries:
        if (current_user.is_authenticated):
        #get progress entries with this training name and current user
            u_progress = TrainingProgress.query.filter(TrainingProgress.u_name == current_user.username).filter(TrainingProgress.t_name == entry.training_name)
            #check if there is an entry present for that
            if (u_progress.count() > 0):
                #if there is, mark flag as completed
                entry.completed = True
            else:
                entry.completed = False

        if (entry.category == 'cryptography'):
            crypto.append(entry)
        elif (entry.category == 'osint'):
            osint.append(entry)
        elif (entry.category == 'steganography'):
            stego.append(entry)
        elif (entry.category == 'general'):
            general.append(entry)
        elif (entry.category == 'web'):
            web.append(entry)
        elif (entry.category == 'forensics'):
            forensics.append(entry)
        else:
            #nothing? error occured
            print('Error occurred, category unknown')

    return render_template('training.html', training_entries=training_entries, crypto=crypto, osint=osint, stego=stego, general=general, web=web, forensics=forensics, title='Training')

@app.route("/profile")
def profile():
    return render_template('profile.html', title='Your Profile')

@app.route("/stories/<string:story>")
def story_chapters(story):
    session['url'] = url_for('story_chapters', story=story)
    file_name = "/stories/" + story + "/" + story + ".html"
    title = story
    return render_template(file_name, title="")


@app.route("/stories/<string:story>/chapter/<int:chapter>")
def story_redirect(story, chapter):
    file_name = "/stories/" + story + "/" + story + "-chapter-" + str(chapter) + ".html"
    title = "Chapter " + str(chapter)
    return render_template(file_name, title=title)



@app.route("/training/<string:training_name>/", methods=['GET'])
def training_redirect(training_name):
    session['url'] = url_for('training_redirect', training_name=training_name)

    training = Training.query.filter(Training.training_name == training_name)
    training = Training.query.get_or_404(training_name)
    file_name = "/training/"+training_name+ "/" + training_name + "-1.html"
    return render_template(file_name, training=training, current_page=1) #get t_name to return training


@app.route("/training/<string:training_name>/<int:page>", methods=['GET'])
def training_page_redirect(training_name, page):
    session['url'] = url_for('training_page_redirect', training_name=training_name, page=page)

    file_name = "/training/"+training_name+ "/" + training_name + "-" + str(page) + ".html"
    training = Training.query.filter(Training.training_name == training_name).first()
    return render_template(file_name, training=training, current_page=page) 


'''
@app.route("/training/<string:training_name>/challenge", methods=['GET'])
def challenge(training_name):
    print("Checking training name...")
    print(training_name)
    #session['url'] = url_for('training_redirect', training_name=training_name)
    file_name = "/training/"+training_name+ "/" + training_name + "-challenge.html"
    print("Checking file name....")
    print(file_name)
    training = Training.query.filter(Training.training_name == training_name).first()
    return render_template(file_name, training=training)


@app.route("/training/<string:training_name>/challenge/success", methods=['GET'])
def challenge_success(training_name):
    #session['url'] = url_for('training_redirect', training_name=training_name)
    file_name = "/training/"+training_name+ "/" + training_name + "-success.html"
    training = Training.query.filter(Training.training_name == training_name).first()
    return render_template(file_name, training=training)
'''

@app.route("/scoreboard")
def scoreboard():
    session['url'] = url_for('scoreboard')   

    topscorers = User.query.order_by(User.points.desc()).limit(10).all()
    
    if (current_user.is_authenticated):
        #What is the current user's scoreboard position
        user_pos = User.query.filter(User.points>=current_user.points).count()
        
        #check every user in top_scorers, if not there, add to the bottom
        top10 = False
        for each_user in topscorers:
            if (each_user == current_user):
                top10 = True
        if not top10: 
            topscorers.append(current_user)


    return render_template('scoreboard.html', topscorers=topscorers, title='Scoreboard')

@app.route("/education")
def education():
    return render_template('/education/teacher-site.html', title='CyberQuest For Education')



def set_points(current_training):
    #if user is logged in
    if (current_user.is_authenticated):
        #Check training completion 
        u_progress = TrainingProgress.query.filter(TrainingProgress.u_name == current_user.username).filter(TrainingProgress.t_name == current_training)
        #if set
        if (u_progress.count() > 0):
             #preview message says you have not earned points
            message = "Already Completed"
        else:
           #change preview message on next page to say that you earned points
            message = "Points"
            #add training competion database entry
            completed_training = TrainingProgress(u_name=current_user.username, t_name=current_training)
            db.session.add(completed_training)
            #add points
            #find points for current training
            training = Training.query.get(current_training)
            current_user.points += training.points
            db.session.commit()
    else:
        message = "No Login"
    return message


@app.route("/training/manual-cracking/challenge", methods=['GET','POST'])
def manual_cracking_challenge():
    form = PasswordCracking1()
    message = "No Login"

    if form.validate_on_submit():
        if (form.username.data == 'admin' and form.password.data == '123456'):
            #call set points and message function
            message = set_points("manual-cracking")
            return render_template('training/manual-cracking/manual-cracking-success.html', message=message) #this keeps the url at the same place!! very useful
        flash('Invalid username or password.')
    return render_template('training/manual-cracking/manual-cracking-challenge.html', form=form)

@app.route("/training/manual-cracking/challenge/success")
def manual_cracking_challenge_success():
    #Must check if we have routed here from the challenge page correctly,
    #if not it should tell the user they can't do that
    return render_template('training/manual-cracking/manual-cracking-success.html')




@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You need to login first")
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    print("")
    print(app.instance_path)
    print(app.root_path)
    return render_template('500.html'), 500



