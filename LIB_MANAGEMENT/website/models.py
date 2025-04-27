from .extensions import db, bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def default_due_date():
    return datetime.utcnow() + timedelta(days=14)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="member")  

    def generate_token(self):
        return create_access_token(identity={"id": self.id, "role": self.role})

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_pass = db.Column(db.String(255), nullable=False)  
    admin_phonenumber = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="admin")

    def __repr__(self):
        return f"<Admin {self.admin_name}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    available_copies = db.Column(db.Integer, default=1)

    def __init__(self, title, author, isbn, available_copies=1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available_copies = available_copies

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=default_due_date)
    returned = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="borrowed_books")
    book = db.relationship("Book", backref="borrow_records")

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id