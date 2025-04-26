from flask import Blueprint, render_template, redirect, flash, request, url_for, session
from .models import User, Book
from .extensions import db
from .decorators import member_required, admin_required

views = Blueprint('views', __name__)

@views.route('/member/homepage')
def member_homepage():
    return render_template('member_home.html')

@views.route('/admin/homepage')
def admin_homepage():
    members = User.query.filter_by(role='member').all()
    books = Book.query.all() 
    return render_template('admin_home.html', members=members, books=books)

@views.route('/admin/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = User.query.get_or_404(member_id)
    if member.role != 'member':
        flash("You can only delete members.", "warning")
        return redirect(url_for('views.admin_homepage'))

    db.session.delete(member)
    db.session.commit()
    flash(f"Member {member.name} has been deleted.", "success")
    return redirect(url_for('views.admin_homepage'))

@views.route('/admin/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = User.query.get_or_404(member_id)
    if member.role != 'member':
        flash("You can only edit members.", "warning")
        return redirect(url_for('views.admin_homepage'))

    if request.method == 'POST':
        member.name = request.form.get('name').strip()
        member.email = request.form.get('email').strip()
        member.phone_number = request.form.get('phone_number').strip()

        try:
            db.session.commit()
            flash("Member updated successfully!", "success")
            return redirect(url_for('views.admin_homepage'))
        except Exception as e:
            db.session.rollback()
            flash(f"Update failed: {str(e)}", "danger")

    return render_template('edit_member.html', member=member)

@views.route('/add-book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    available_copies = request.form.get('available_copies')

    if not title or not author or not isbn:
        flash('Please fill in all required fields.', category='error')
        return redirect(url_for('views.admin_homepage'))  
    
    new_book = Book(
        title=title,
        author=author,
        isbn=isbn,
        available_copies=int(available_copies) if available_copies else 1
    )

    db.session.add(new_book)
    db.session.commit()
    flash('Book added successfully!', category='success')

    return redirect(url_for('views.admin_homepage'))

@views.route('/admin/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id) 
    db.session.delete(book)  
    db.session.commit()  
    return redirect(url_for('views.admin_homepage'))

@views.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.available_copies = request.form['available_copies']

        db.session.commit()
        flash('Book edited successfully!', category='success')

        return redirect(url_for('views.admin_homepage'))

    return render_template('edit_book.html', book=book)