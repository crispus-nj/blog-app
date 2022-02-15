from flask import Blueprint, redirect, render_template, url_for, request, flash
import requests
from flask_login import login_required, current_user
from app.posts.forms import PostQuoteForm, UpdatePostForm
from app.models import Post
from app import db

posts = Blueprint('posts', __name__)


@posts.route('/user-posts')
def view_posts():
    post_page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_time.desc()).paginate(page=post_page, per_page=4)
    
    return render_template('view_posts.html', posts=posts)


@posts.route('/most-popular')
def popular_posts():
    posts = requests.get('http://quotes.stormconsultancy.co.uk/quotes.json')
    posts = posts.json()
    
    return render_template('most_popular.html', posts=posts)

@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostQuoteForm()
    if form.validate_on_submit():
        post = Post(quote = form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Quote created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form)

@posts.route('/post/<post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    form = UpdatePostForm()
    post = Post.query.get(post_id)
    if form.validate_on_submit():
        post.quote = form.content.data
        db.session.commit()
        flash('Quote updated successfull', 'success')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        form.content.data = post.quote 
    
    return render_template('update_post.html', form=form, post_id = post)

@posts.route('/post/<post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Quote Delete successfully', 'success')
    return redirect(url_for('main.home'))



# @app.route('/posts/<post_id>/comment', methods=['GET', 'POST'])
# def comments(post_id):
#     posts = Post.query.get_or_404(post_id)
#     # form = CommentForm()
#     # if form.validate_on_submit():
#         # comment = Comment(comment = form.comment.data, post_id=posts.id, user_id=current_user)
#         # db.session.add(comment)
#         # db.session.commit()
#         # return redirect(url_for('view_posts'))
#     print(post_id)
#     return render_template('view_posts.html')


###########################
###### POSTS ROUTES #########
###########################


# @app.route('//<post_id>/comments', methods=['GET', 'POST'])
# def comments(post_id):
#     posts = Post.query.get_or_404(post_id)
#     posts_id = request.args.get("posts_id")
#     comments = request.form.get('comment')
#     form = CommentForm()
#     if form.validate_on_submit():
#         pass
#     # print(current_user.id)
#     if comments:
#         comment = Comment(user_id=current_user.id,post_id = posts_id,comment = comments, user=posts_id)
#         # print(comment)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('view_posts'))
#     return redirect(url_for('view_posts'))
