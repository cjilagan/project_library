import os
from flask import Blueprint, render_template, redirect, flash, request, url_for, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Admin, User
from .extensions import db
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint('auth', __name__)

VALID_ADMIN_KEY = os.getenv("ADMIN_SECRET_KEY")


@auth.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = Admin.query.filter_by(admin_email=email).first()
        print(existing_user)

        if existing_user:
            if check_password_hash(existing_user.admin_pass, password):  
                flash('Logged in Successfully', category='success')
                return redirect('/admin/homepage')
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template('admin_login.html')

@auth.route('/member', methods=['GET', 'POST'])
def member_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, role='member').first()

        if user and check_password_hash(user.password_hash, password):
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.member_homepage'))
        else:
            flash('Incorrect email or password, try again.', category='error')

    return render_template('member_login.html')




@auth.route('/member/signup', methods=['GET', 'POST'])
def member_signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        phone_number = request.form.get('phone_number', '').strip()

        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return render_template('member_signup.html', name=name, email=email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered.", "danger")
            return render_template('member_signup.html', name=name, email=email)

        hashed_password = generate_password_hash(password)

        new_member = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            phone_number=phone_number,
            role='member'  
        )

        try:
            db.session.add(new_member)
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}", "danger")

    return render_template('member_signup.html')

@auth.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    admin_email = ""
    admin_name = ""

    if request.method == 'POST':
        admin_name = request.form.get('admin_name', '').strip()
        admin_email = request.form.get('email', '').strip()
        admin_pass = request.form.get('password', '').strip()
        admin_phonenumber = request.form.get('phone_number', '').strip()
        admin_secret_key = request.form.get('admin_secret_key', '').strip()  

        print(f"Received: {admin_name}, {admin_email}, {admin_pass}, {admin_phonenumber}, {admin_secret_key}")

        if not VALID_ADMIN_KEY:
            flash("Admin secret key is missing from the server configuration.", "danger")
            return render_template('admin_create_account.html', admin_email=admin_email, admin_name=admin_name)

        if admin_secret_key != VALID_ADMIN_KEY:
            flash("Invalid admin registration key.", "danger")
            return render_template('admin_create_account.html', admin_email=admin_email, admin_name=admin_name)
            
        if not admin_email or not admin_pass:
            flash("Email and password are required.", "danger")
            return render_template('admin_create_account.html', admin_email=admin_email, admin_name=admin_name)

        existing_admin = Admin.query.filter_by(admin_email=admin_email).first()
        if existing_admin:
            flash("Email is already registered.", "danger")
            return render_template('admin_create_account.html', admin_email=admin_email, admin_name=admin_name)

        hashed_password = generate_password_hash(admin_pass, method='pbkdf2:sha256')

        new_admin = Admin(
            admin_name=admin_name,
            admin_email=admin_email,
            admin_pass=hashed_password,
            admin_phonenumber=admin_phonenumber,
        )

        try:
            db.session.add(new_admin)
            db.session.commit()
            flash("Admin account created successfully!", "success")
            return redirect(url_for('auth.login')) 
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
