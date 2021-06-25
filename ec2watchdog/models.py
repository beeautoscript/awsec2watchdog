from datetime import datetime
from enum import unique
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ec2watchdog import app,db

#AccessKey Data Model
class AccessKey(db.Model):
    __bind_key__ = 'accesskey'
    id = db.Column(db.Integer,primary_key=True)
    keyname = db.Column(db.String(10),unique=True,nullable=False)
    accesskeyid = db.Column(db.String(20),unique=True,nullable=False)
    secretkeyid = db.Column(db.String(40),unique=True,nullable=False)

    def __repr__(self) -> str:
        return f"{self.keyname},{self.accesskeyid},{self.secretkeyid}"