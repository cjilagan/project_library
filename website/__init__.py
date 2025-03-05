import eventlet
eventlet.monkey_patch()
from flask import Flask
from .extensions import db, migrate, login_manager, ip_address, save_data

from os import path
import os
import pymysql



pymysql.install_as_MySQLdb()


def create_website():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["JWT_SECRET_KEY"] = 'aobwduiao'
  

    app.config["SQLALCHEMY_DATABASE_URI"] = (
          f"mysql+pymysql://root:%40Anday2108@localhost:3306/attendance_db?charset=utf8"
    )
     # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') For deployment


    from .auth import auth
    app.register_blueprint(auth)



    db.init_app(app)

    migrate.init_app(app, db)
     


    create_database(app)

    return app


def create_database(app):

    with app.app_context():
        db.create_all()
        print("Created Database!")