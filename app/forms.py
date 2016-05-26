from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None


class RegisterForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
	email = StringField('username', validators=[DataRequired()]) 

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

