from flask import Blueprint, render_template
from .decorators import member_required

views = Blueprint('views', __name__)

@views.route('/member/homepage')
@member_required
def member_homepage():
    return render_template('member_home.html')

@views.route('/admin/homepage')
@admin_required
def admin_homepage():
    return render_template('admin_home.html')
