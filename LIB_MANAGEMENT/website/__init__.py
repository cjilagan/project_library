from flask import Flask
from .extensions import db, migrate, login_manager, ip_address, save_data, bcrypt
from .models import User
from flask_migrate import Migrate
import pymysql
from sqlalchemy import text  

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'aobwduiao'  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///library.db'


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth  
    app.register_blueprint(auth)  

    from .views import views
    app.register_blueprint(views)

    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))  
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")


    create_database(app)

    return app  

def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created Database!")