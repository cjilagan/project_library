from flask import Blueprint, render_template, redirect, flash, request, url_for, session, jsonify
from werkzeug.security import check_password_hash
from website.models import Admin, Student
from .extensions import db, bcrypt
import pymysql

auth = Blueprint('auth', __name__)

# ✅ Function to establish a MySQL database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Change if needed
        password="2108",  # Change if needed
        database="libmanagement"
    )

# ✅ Admin Login Route
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and check_password_hash(existing_user.password, password):
            session.permanent = True  
            session['user_id'] = existing_user.id  
            session['role'] = existing_user.role  # ✅ Store role in session
            flash("Login successful!", "success")

            if existing_user.role == "admin":
                return redirect(url_for('views.admin_homepage'))
            else:
                return redirect(url_for('views.member_homepage'))  # Redirect members to a different page

        flash('Invalid email or password.', 'danger')

    return render_template('index.html')

# ✅ Admin Homepage Route
@auth.route('/homepage', methods=['GET'])
def home():
    return render_template('index.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    email = ""
    admin_name = ""

    if request.method == 'POST':
        admin_name = request.form.get('admin_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        school_name = request.form.get('school_name', '').strip()
        department_name = request.form.get('department_name', '').strip()

        
        print(f"Received: {admin_name}, {email}, {password}, {phone_number}, {school_name}, {department_name}")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template('admin_create_account.html', email=email, admin_name=admin_name)

        
        existing_user = Admin.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered.", "danger")
            return render_template('admin_create_account.html', email=email, admin_name=admin_name)

       
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
        new_admin = Admin(
            admin_name=admin_name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            school_name=school_name,
            department_name=department_name
        )

        try:
            db.session.add(new_admin)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('auth.admin_login'))  # Redirect to login page
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}", "danger")

    return render_template('admin_create_account.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)  
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
