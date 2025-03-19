from flask import Flask
from .extensions import db, migrate, login_manager, ip_address, save_data
from flask_migrate import Migrate
import os
import pymysql
from sqlalchemy import text  

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'aobwduiao'  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///library.db'


    # ✅ Initialize database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Import blueprints inside the function to avoid circular imports
    from .auth import auth  
    app.register_blueprint(auth)  

    # ✅ Test database connection
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))  
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")

    # ✅ Create tables if not exist
    create_database(app)

    return app  

def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created Database!")
