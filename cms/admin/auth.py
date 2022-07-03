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