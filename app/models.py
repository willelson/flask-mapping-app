from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(30))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    routes = db.relationship('Route', cascade="all, delete-orphan", backref='user', lazy='dynamic')

    def __init__(self , username ,password , email):
        self.username = username
        self.password = generate_password_hash(password)
        # self.set_password(password)
        self.email = email
        self.registered_on = datetime.now()

    def check_password(self, password):
            return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.id)



class Route(db.Model):
    """One to many relationship with user"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    route_info = db.relationship('RouteInfo', cascade="all, delete-orphan", backref='route', lazy='dynamic')
    name = db.Column('name' , db.String(10))

class RouteInfo(db.Model):
    """One to many relationship with route"""
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)







#