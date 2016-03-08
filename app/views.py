from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
# from .forms import LoginForm
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Handle what happens when unauthorised user tries to acces a page where login_required
@lm.unauthorized_handler
def unauthorized():
    flash("You must be log in first!")
    return redirect('login')

# functions that are decorated with before_request will run before the view 
# function each time a request is received
@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')