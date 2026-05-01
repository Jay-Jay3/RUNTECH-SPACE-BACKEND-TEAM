# This is the python file for handling the database schema (SQLAlchemy)
"""
        That means all functions, methods and classes involving the strcuture of the database will 
        be done here.....
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Compliant(db.Model):
    __tablename__ = "complaint"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(20), default ="Pending")
    created_at = db.Column(db.DateTime,default=datetime.now(), onupdate=datetime.now())
    admin_response = db.Column(db.Text, default="Not Responded Yet")
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    

