from flask import Blueprint, Flask, render_template, redirect
from .extensions import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():

    new_user = User(name = 'anne')
    db.session.add(new_user)
    db.session.commit()
    return 'Hello world'

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('index.html')