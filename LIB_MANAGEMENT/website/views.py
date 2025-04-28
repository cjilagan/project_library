from flask import Blueprint, render_template, redirect, flash, request, url_for, session
from flask_login import current_user, login_required
from .models import User, Book, BorrowRecord, BorrowRequest
from .extensions import db, login_manager
from .decorators import member_required, admin_required

views = Blueprint('views', __name__)

@views.route('/member/homepage')
@login_required
def member_homepage():
    books = Book.query.all()
    borrowed_books = BorrowRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('member_home.html', books=books, borrowed_books=borrowed_books)

@views.route('/admin/homepage')
@login_required
def admin_homepage():
    members = User.query.filter_by(role='member').all()
    books = Book.query.all()
    borrow_requests = BorrowRequest.query.filter_by(status='pending').all() 
    return render_template('admin_home.html', members=members, books=books, borrow_requests=borrow_requests)

@views.route('/admin/accept_request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    request_record = BorrowRequest.query.get_or_404(request_id)
    book = Book.query.get(request_record.book_id)

    if book and book.available_copies > 0:
        book.available_copies -= 1
        borrow_record = BorrowRecord(user_id=request_record.user_id, book_id=request_record.book_id)
        request_record.status = 'accepted'
        db.session.add(borrow_record)
        db.session.commit()
        flash('Request accepted and book borrowed!', 'success')
    else:
        flash('Book not available.', 'error')
    return redirect(url_for('views.admin_homepage'))

@views.route('/admin/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    request_record = BorrowRequest.query.get_or_404(request_id)
    request_record.status = 'rejected'
    db.session.commit()
    flash('Request rejected.', 'info')
    return redirect(url_for('views.admin_homepage'))

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

    existing_book = Book.query.filter_by(isbn=isbn).first()
    if existing_book:
        flash('A book with this ISBN already exists!', 'error')
        return redirect(url_for('views.admin_homepage'))

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

@views.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if not current_user.is_authenticated:
        flash('Please log in to borrow books.', 'error')
        return redirect(url_for('auth.login'))  # adjust to your login page

    book = Book.query.get_or_404(book_id)
    borrowed_count = BorrowRecord.query.filter_by(user_id=current_user.id, returned=False).count()

    if borrowed_count >= 3:  
        flash('Borrow limit reached (3 books). Return a book first!', 'error')
        return redirect(url_for('views.member_homepage'))
    
    if book.available_copies > 0:
        book.available_copies -= 1
        borrowed = BorrowRecord(
            user_id=current_user.id,
            book_id=book.id
        )

        db.session.add(borrowed)
        db.session.commit()
        flash(f"You have borrowed {book.title}! Due by {borrowed.due_date.date()}", "success")
    else:
        flash(f"Sorry, {book.title} is not available.", "error")

    return redirect(url_for('views.member_homepage'))

@views.route('/request_borrow/<int:book_id>', methods=['POST'])
def request_borrow(book_id):
    book = Book.query.get_or_404(book_id)
    existing_request = BorrowRequest.query.filter_by(user_id=current_user.id, book_id=book_id, status='pending').first()
    
    if existing_request:
        flash('You have already requested this book.', 'error')
        return redirect(url_for('views.member_homepage'))
    
    new_request = BorrowRequest(user_id=current_user.id, book_id=book_id)
    db.session.add(new_request)
    db.session.commit()

    flash('Borrow request sent! Please wait for admin approval.', 'success')
    return redirect(url_for('views.member_homepage'))