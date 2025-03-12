from flask import Flask
from .extensions import db, migrate, login_manager, ip_address, save_data
from flask_migrate import Migrate
from os import path
import os
import pymysql


pymysql.install_as_MySQLdb()



def create_website():


    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["SECRET_KEY"] = 'aobwduiao'

    app.config["SQLALCHEMY_DATABASE_URI"] = ('mysql://root:cjilagansql@localhost/users')
     # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') For deployment
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    from .auth import auth
    app.register_blueprint(auth)


    db.init_app(app)
    migrate.init_app(app, db)
    migrate(app, db)
     
    from sqlalchemy import text  # ✅ Import text


    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))  # ✅ Use text() for raw SQL
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")


    create_database(app)


    return app




def create_database(app):


    with app.app_context():
        db.create_all()
        print("Created Database!")
