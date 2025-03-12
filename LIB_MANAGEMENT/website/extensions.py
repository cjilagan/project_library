from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

ip_address = ""


def save_data(data):


     try:
          db.session.add(data)
          db.session.commit()


          return('success')
     except:
          db.session.rollback()
          return('failed')
