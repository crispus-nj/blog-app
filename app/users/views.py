from flask import Blueprint, redirect, render_template, request, flash, url_for
from app.users.forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from app import db
from app.models import User


users = Blueprint('users', __name__)

@users.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"{user.username} logged in!", 'success')
            nex_page = request.args.get('next')
            return redirect(nex_page) if nex_page else redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@users.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username = form.username.data,
                    password = generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully, Log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

