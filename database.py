from flask import Flask, render_template, request, redirect, url_for, session, g
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///empmanagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False)

    def __init__(self, name, password, admin=0):
        self.name = name
        self.password = password
        self.admin = admin


class emp(db.Model):
    empid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    joining_date = db.Column(db.Date, unique=False, nullable=False)
    total_projects = db.Column(db.Integer, unique=False, nullable=False)
    total_test_case = db.Column(db.Integer, unique=False, nullable=False)
    total_defect_found = db.Column(db.Integer, unique=False, nullable=False)
    total_defects_pending = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, name, email, phone, address, total_projects=1, total_test_case=5,
                 total_defect_found=1, total_defects_pending=1):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.joining_date = date.today()
        self.total_projects = total_projects
        self.total_test_case = total_test_case
        self.total_defect_found = total_defect_found
        self.total_defects_pending = total_defects_pending
