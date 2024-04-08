
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


base_bp = Blueprint("base", __name__)

# Form for posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Route for home page
@base_bp.route("/")
@login_required
def home():
    posts = Post.query.all()  # fetch all posts from the database
    return render_template('index.html', posts=posts)

# Route for creating a new post
@base_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Post(title=title, body=body, author_id=current_user.id)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return 'There was an issue adding your post'

    else:
        return render_template('create.html')

# Route for viewing a post
@base_bp.route('/view/<int:id>', methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view.html', post=post)

# Route for requesting to join a post
@base_bp.route('/request_join/<int:id>', methods=['POST'])
def request_join(id):
    post = Post.query.get_or_404(id)
    flash('The owner of this opportunity has been notified and will be in touch as soon as possible.', 'info')
    return redirect(url_for('base.home'))

# Route for editing a post
@base_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('base.home'))

    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    return render_template('update.html', form=form)

# Route for deleting a post
@base_bp.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was successfully deleted')
    return redirect(url_for('base.home'))