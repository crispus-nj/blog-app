from flask import redirect, url_for, flash, render_template
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home():
    flash('Application started successfully', 'success')
    return render_template("index.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)