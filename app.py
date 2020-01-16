import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Member(db.Model):

    id = db.Column(db.LargeBinary(length=16), unique=True, primary_key=True)
    liuid = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)


    def __init__(self, liuid, email, **kwargs):
        super(Member, self).__init__(**kwargs)

        self.id = uuid.uuid4().bytes
        self.liuid = liuid
        self.email = email


    def __repr__(self):
        return "<id={}, liuid={}, email={}>"\
                .format(str(uuid.UUID(bytes=self.id)), self.liuid, self.email)
