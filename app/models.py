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

    # Variables to describe the bounds of all the users routes
    NElat = db.Column(db.Float)
    NElng = db.Column(db.Float)
    SWlat = db.Column(db.Float)
    SWlng = db.Column(db.Float)

    def updateBounds(self):
        # NElng & SWlat not getting set
        # print self.NElng, self.NElat, self.SWlng, self.SWlat
        for route in Route.query.filter_by(user=self).all():
            # print "route: {0} | {1} | {2} | {3}".format(route.NElat, route.NElng, route.SWlat, route.SWlng)
            # print "SWlat: {0} | {1} | {2}".format(route.SWlat < self.SWlat, route.SWlat == None)
            if route.NElat > self.NElat or self.NElat == None:
                self.NElat = route.NElat 
            if route.NElng < self.NElng or self.NElng == None:
                self.NElng = route.NElng 
            if route.SWlat < self.SWlat or self.SWlat == None:
                self.SWlat = route.SWlat
            if route.SWlng > self.SWlng or self.SWlng == None:
                self.SWlng = route.SWlng
            print "user: {0} | {1} | {2} | {3} \n".format(self.NElat, self.NElng, self.SWlat, self.SWlng)
        print self.SWlat == None
        print Route.query.filter_by(user=self).all()

    def __init__(self , username ,password , email):
        self.username = username
        self.password = generate_password_hash(password)
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

    # Variables to describe the bound of the route
    NElat = db.Column(db.Float)
    NElng = db.Column(db.Float)
    SWlat = db.Column(db.Float)
    SWlng = db.Column(db.Float)

class RouteInfo(db.Model):
    """One to many relationship with route"""
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)



# >>> user = models.User.query.filter_by(username="will").first()
# >>> route2 = models.Route(name="Ladybower", user=user)
# >>> point1 = models.RouteInfo(longitude=53.3573457, latitude=-1.698183, elevation=203.4, route_id=route2.id)
# >>> point2 = models.RouteInfo(longitude=53.3572457, latitude=-1.698209, elevation=203.8, route_id=route2.id)
# >>> db.session.add(point1)
# >>> db.session.add(point2)
# >>> db.session.commit()
# >>> print user.routes.all()





#