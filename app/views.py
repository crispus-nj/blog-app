from flask import redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app import app , db
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/')
def home():
    db.create_all()
    return render_template("index.html")

###########################
######USERS ROUTES#########
###########################

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"{user.username} logged in!", 'success')
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username = form.username.data,
                    password = generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully, Log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    