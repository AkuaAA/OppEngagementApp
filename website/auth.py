from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .extension import db, bcrypt
from .models import Employee
from .forms import RegisterForm, LoginForm
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_HOURS = 1

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("base.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user:
            if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                if not form.recaptcha.validate(form):
                    flash("Please complete the reCAPTCHA.", "danger")
                    return render_template("login.html", form=form)
                if datetime.now() < user.account_lockout_until:
                    flash("Account locked. Please wait and try again later.", "danger")
                    return render_template("login.html", form=form)
                else:
                    # Reset failed login attempts after lockout period
                    user.failed_login_attempts = 0
                    user.account_lockout_until = None
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("base.home"))
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                    # Set account lockout time
                    user.account_lockout_until = datetime.now() + timedelta(hours=LOCKOUT_HOURS)
                db.session.commit()
                flash("Invalid email and/or password.", "danger")
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