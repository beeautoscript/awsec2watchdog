from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length,ValidationError
from ec2watchdog.models import AccessKey


#Add AccessKey Form
class AddAccessKeyForm(FlaskForm):
    keyname = StringField('Key Name',validators=[DataRequired(),Length(min=2,max=50)])
    access_keyid = StringField('Access Key Id',validators=[DataRequired(),Length(min=20,max=20)])
    secret_keyid = PasswordField('Secret Access Key',validators=[DataRequired(),Length(min=40,max=40)])
    submit = SubmitField('Add Key')