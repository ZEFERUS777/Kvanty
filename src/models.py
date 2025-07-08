from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class Groups(db.Model, SerializerMixin):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), nullable=False, unique=True)
    tuitor = db.Column(db.String(128), nullable=False)
    Students = db.Column(db.Text)
    lead_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Students(db.Model, SerializerMixin):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))


class Rules(db.Model, SerializerMixin):
    __tablename__ = "rules"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)


class Users(db.Model, UserMixin, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    rule = db.Column(db.Integer, db.ForeignKey("rules.id"))
    lead_group = db.Column(db.Integer, db.ForeignKey("groups.id"))
    group_rate = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Home_Work(db.Model, SerializerMixin):
    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(128), nullable=False)
    task = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))


class Works(db.Model, SerializerMixin):
    __tablename__ = "works"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    work = db.Column(db.Text)
    add_date = db.Column(db.DateTime, default=datetime.utcnow())
    homework_name = db.Column(db.Integer, db.ForeignKey("homework.id"))
    Credited = db.Column(db.Integer, default=0)