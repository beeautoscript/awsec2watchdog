from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField
from wtforms import validators
from wtforms import StringField,SelectField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,IPAddress

#EC2 SSH form
class Ec2SshForm(FlaskForm):
	hostname = StringField('hostname',render_kw={'readonly': True},validators=[DataRequired(),IPAddress(ipv4=True,message="Please enter valid public ipv4 address")])
	username = StringField('username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	title = StringField('title',validators=[DataRequired()])
	submit = SubmitField('Connect')


#EC2 Region
class Ec2FilterForm(FlaskForm):
    awsregion = SelectField('Region',choices=[('us-east-1','US East (N. Varginia)'),('us-east-2','US East (Ohio)'),
		('us-west-1','US West (N. California)'),('us-west-2','US West (Oregon)'),('af-south-1','Africa (CapeTown)'),
		('ap-east-1','Asia Pacific (Hong Kong)'),('ap-south-1','Asia Pacific (Mumbai)'),('ap-northeast-2','Asia Pacific (Seoul)'),
		('ap-southeast-1','Asia Pacific (Singapore)'),('ap-southeast-2','Asia Pacific (Sydney)'),
		('ap-northeast-1','Asia Pacific (Tokyo)'),('ca-central-1','Canada (Central)'),('eu-central-1','Europe (Frankfurt)'),
		('eu-west-1','Europe (Irekand)'),('eu-west-2','Europe (London)'),('eu-south-1','Europe (Milan)'),
		('eu-west-3','Europe (Paris)'),('eu-north-1','Europe (Stockholm)'),('me-south-1','Middle East (Bahrin)')])
		
    submit = SubmitField('Load EC2 instances')