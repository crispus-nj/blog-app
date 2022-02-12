from flask import redirect, url_for, flash, render_template
from app import app

@app.route('/')
def home():
    flash('Application started successfully', 'success')
    return render_template("index.html")