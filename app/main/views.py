from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import Post
import requests
from app.main.forms import SuscribeForm
from app.main.utils import send_mail


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    db.create_all()
    form = SuscribeForm()
    post_page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_time.desc()).paginate(page=post_page, per_page=1)
    posts_data = requests.get('http://quotes.stormconsultancy.co.uk/quotes.json')
    posts_data = posts_data.json()

    if form.validate_on_submit():
        email = form.content.data
        send_mail(email)
        flash('Mail Sent successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template("index.html", posts = posts, posts_data=posts_data, form=form)