from flask import redirect, url_for, flash, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from app import app , db
from app.forms import LoginForm, RegisterForm, PostQuoteForm
from app.models import User, Post
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
            nex_page = request.args.get('next')
            return redirect(nex_page) if nex_page else redirect(url_for('home'))
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


###########################
######POSTS ROUTES#########
###########################
@app.route('/most-popular')
def popular_posts():
    posts = requests.get('http://quotes.stormconsultancy.co.uk/quotes.json')
    
    return render_template('most_popular.html', posts=posts)

@app.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostQuoteForm()
    if form.validate_on_submit():
        post = Post(quote = form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Quote created', 'success')
        return redirect(url_for('home'))
        # Java programming is used for mobile application. sweet for trail if you have the sike of a bee!
    return render_template('create_post.html', form=form)