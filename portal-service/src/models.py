from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    hashed_password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="normalUser")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    medical_certificate = db.Column(db.String(), nullable=False)
    gpa = db.Column(db.Integer, nullable=False)
    flight_hours = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), default = "submitted")
    