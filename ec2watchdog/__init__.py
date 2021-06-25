from flask import Flask
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

#App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accesskey.db'
app.config['SQLALCHEMY_BINDS'] = {'accesskey':'sqlite:///accesskey.db'}
db = SQLAlchemy(app)

#Import Blueprint routes objects
from ec2watchdog.home.routes import blue
from ec2watchdog.add_awsaccesskey.routes import blue
from ec2watchdog.load_ec2.routes import blue, loadec2

#Register Blueprint
app.register_blueprint(home.routes.blue)
app.register_blueprint(add_awsaccesskey.routes.blue)
app.register_blueprint(load_ec2.routes.blue)