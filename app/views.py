from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, RegisterForm
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Handle what happens when unauthorised user tries to acces a page where login_required
@lm.unauthorized_handler
def unauthorized():
    flash("You must log in first!")
    return redirect('login')

# functions that are decorated with before_request will run before the view 
# function each time a request is received
@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	# stop user accesing login page if a user is currently logged in
	login = False
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit(): 
		username = form.username.data.strip()
		password = form.password.data
		user = User.query.filter_by(username=username).first()
		if user is not None:
			if user.check_password(password):
				login_user(user)
				login = True
	if login == True:
		return redirect(url_for('index'))			
	else:
		return render_template('login.html',
								form=LoginForm())

@app.route('/register' , methods=['GET','POST'])
def register():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		email = form.email.data
		user = User.query.filter_by(username=username).first()
		if user is None:
			# Create new instance and add to db
			user = User(username, password, email)
			db.session.add(user)
			db.session.commit()
		login_user(user)
		return redirect(url_for('index'))
	else:
		# flash('Invalid login credentials')
		return render_template('register.html',
								form=RegisterForm())



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash('Logout successful!')
	return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template('profile.html');






