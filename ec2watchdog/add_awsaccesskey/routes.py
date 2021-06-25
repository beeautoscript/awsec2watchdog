from flask import Blueprint,render_template,url_for, flash, redirect
from wtforms import form
from ec2watchdog import app,db
from ec2watchdog.add_awsaccesskey.forms import AddAccessKeyForm
from ec2watchdog.models import AccessKey
import boto3
import botocore

#Blueprint object
blue = Blueprint('add_awsaccesskey',__name__,template_folder='templates')

#Add Access Key
@blue.route('/add_awsaccesskey',methods=['GET','POST'])
def add_awsaccesskey():
    form = AddAccessKeyForm()
    if form.validate_on_submit():
        sts = boto3.client('sts',aws_access_key_id=form.access_keyid.data,aws_secret_access_key=form.secret_keyid.data)
        try:
            sts.get_caller_identity()
            accesskey_db = AccessKey(keyname=form.keyname.data,accesskeyid=form.access_keyid.data,secretkeyid=form.secret_keyid.data)
            db.session.add(accesskey_db)
            db.session.commit()
            flash(f'AccessKey Registered Successfully','success')
            return redirect(url_for('home.home'))
        except botocore.exceptions.ClientError:
            flash(f'Invalid AccessKey','danger')
            return redirect(url_for('add_awsaccesskey.add_awsaccesskey'))
    return render_template('add_awsaccesskey/add_awsaccesskey.html',title="Home : Add AWS AccessKey",form=form)