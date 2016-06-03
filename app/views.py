from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, RegisterForm, UploadForm
from .models import User, Route, RouteInfo
import gpxpy 
import gpxpy.gpx 

ALLOWED_EXTENSIONS = set(['txt', 'gpx'])

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
	form = UploadForm();
	if form.validate_on_submit():
		return redirect(url_for('uploader'))

	return render_template('profile.html', form=form);

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		name = request.form['name']
		print name, file
		if file and allowed_file(file.filename) and name != None:
			gpx = gpxpy.parse(file) 
			for track in gpx.tracks: 
				new_route = Route(name=name, user=current_user)
				db.session.add(new_route)
				print "\n new_route.name = {0} \n".format(new_route.name)
				for segment in track.segments: 
					for point in segment.points:
						
						new_point = RouteInfo(longitude=point.longitude, latitude=point.latitude, 
													 elevation=point.elevation, route=new_route)
						db.session.add(new_point)
			db.session.commit()
			print "Upload successfull"
			return redirect(url_for('login'))
		else:
			return 'file upload unsuccessfull'

@app.route('/_get_routes')
def get_routes():
	routes = {}
	for route in current_user.routes:
		routes[route.name] = []
		for point in Route.query.filter_by(route=route).all():
			print "({0},{1})".format(point.longitude, point.latitude)
	return false

@app.route('/_get_coords')
def get_coords():
	name = request.args.get('name')
	route = Route.query.filter_by(name=name, user=current_user).first()
	info = RouteInfo.query.filter_by(route=route).all()
	return_info = []
	maxLat = info[0].latitude;
	minLat = info[0].latitude;
	maxLng = info[0].longitude;
	minLng = info[0].longitude;
	for point in info:
		if point.latitude > maxLat:
			maxLat = point.latitude
		elif point.latitude < minLat:
			minLat = point.latitude
		if point.longitude > maxLat:
			maxLng = point.longitude
		elif point.longitude < minLat:
			minLng = point.longitude
		return_info.append([point.latitude, point.longitude, point.elevation])
	print "\n\nmaxLat: {0} \nminLat: {1} \nmaxLng: {2} \nminLng: {3}\n\n".format(maxLat, minLat, maxLng, minLng)
		
		# print "({0},{1})".format(point.longitude, point.latitude)
	print type(return_info)
	print len(info)
	return jsonify(result=return_info)




# Get data for a users route
# route = models.Route.query.filter_by(name="Test2", user=user).first()
# info = models.RouteInfo.query.filter_by(route=route).all()


