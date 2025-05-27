from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class Groups(db.Model, SerializerMixin):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), nullable=False, unique=True)
    tuitor = db.Column(db.String(128), nullable=False)


class Students(db.Model, SerializerMixin):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))