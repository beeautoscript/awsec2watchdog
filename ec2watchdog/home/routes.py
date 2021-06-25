from os import access
from flask import Blueprint,render_template,url_for, flash, redirect, request
from ec2watchdog import app,db
from ec2watchdog.models import AccessKey

#Blueprint object
blue = Blueprint('home',__name__,template_folder='templates')

#Home
@blue.route('/',methods=('GET','POST'))
def home():
    page = request.args.get('page',1,type=int)
    accesskeydb_len = len(db.session.query(AccessKey).all())
    accesskey_records = AccessKey.query.paginate(page=page,per_page=10)
    return render_template('home/home.html',title='EC2 Watchdog : Home',accesskeydb_len=accesskeydb_len,accesskey_records=accesskey_records)

#Remove Aws AccessKey from Database
@blue.route('/remove/<string:rowid>',methods=('GET','POST'))
def remove_accesskey(rowid):
    row_id = AccessKey.query.get_or_404(rowid)
    db.session.delete(row_id)
    db.session.commit()
    return redirect(url_for('home.home'))