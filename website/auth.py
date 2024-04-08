from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .extension import db, bcrypt
from .models import Employee
from .forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("base.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("base.home"))
        else:
            flash("Invalid email and/or password.", "danger")
    return render_template("login.html", form=form)

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("base.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Employee(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for('auth.login'))