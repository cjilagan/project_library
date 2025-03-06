from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
login_manager = LoginManager()


ip_address = ""


def save_data(data):

     try:
          db.session.add(data)
          db.session.commit()

          return('success')
     except:
          db.session.rollback()
          return('failed')