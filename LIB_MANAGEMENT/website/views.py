from flask import Blueprint, render_template, redirect, flash, request, url_for, session
from .models import User
from .extensions import db
from .decorators import member_required, admin_required

views = Blueprint('views', __name__)

@views.route('/member/homepage')
def member_homepage():
    return render_template('member_home.html')

@views.route('/admin/homepage')
def admin_homepage():
    members = User.query.filter_by(role='member').all()
    return render_template('admin_home.html', members=members)

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

