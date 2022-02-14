from flask import redirect, url_for, flash, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from app import app , db
from app.forms import LoginForm, RegisterForm, PostQuoteForm, UpdatePostForm, CommentForm
from app.models import User, Post, Comment
from flask_login import login_user, login_required, logout_user, current_user




###########################
###### MAIN ROUTES #########
###########################
@app.route('/')
def home():
    db.create_all()
    post_page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_time.desc()).paginate(page=post_page, per_page=1)
    # for post in posts:
    #     print(post.quote)
    #     print(current_user.username)
    #     print(type(post))
    return render_template("index.html", posts = posts)

###########################
###### USERS ROUTES #########
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

@app.route('/<post_id>/comment', methods=['POST', 'GET'])
def comment(post_id):
    posts = Post.query.get_or_404(post_id)
    comment_post = posts.id
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment = form.content.data, comment_post=posts.id )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form=form)


###########################
###### POSTS ROUTES #########
###########################
@app.route('/most-popular')
def popular_posts():
    posts = requests.get('http://quotes.stormconsultancy.co.uk/quotes.json')
    posts = posts.json()
    
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
    return render_template('create_post.html', form=form)

@app.route('/post/<post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    form = UpdatePostForm()
    post = Post.query.get(post_id)
    if form.validate_on_submit():
        post.quote = form.content.data
        db.session.commit()
        flash('Quote updated successfull', 'success')
        return redirect(url_for('home'))
    if request.method == 'POST':
        form.content.data = post.quote 
    
    return render_template('update_post.html', form=form, post_id = post)

@app.route('/post/<post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Quote Delete successfully', 'success')
    return redirect(url_for('home'))