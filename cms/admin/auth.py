from cms.admin import admin_bp
from cms.admin.models import User
from flask import render_template, request, redirect, url_for, flash, session, g
from functools import wraps

def protected(route_function):
    @wraps(route_function)
    def wrapped_route_function(**kwargs):
        if g.user is None:
            return redirect(url_for('admin.login'))
        return route_function(**kwargs)
    return wrapped_route_function

@admin_bp.before_app_request
def load_user():
    user_id= session.get('user_id')
    g.user= User.query.get(user_id) if user_id is not None else None

@admin_bp.route('/login', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username= request.form['username']
        password= request.form['password']

        error= None
        user= User.query.filter_by(username=username).first()
        if user is None:
            error= "user wrong"
        elif not user.check_password(password):
            error= "password wrong"
        if error is None:
            session.clear()
            session['user_id']= user.id
            return redirect(url_for('admin.content', type = 'page'))
        flash(error)

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))