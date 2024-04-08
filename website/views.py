from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .extension import db
from .models import Post

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author_id or not current_user.is_superuser:
        flash('You do not have permission to edit this post.', 'error')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    return render_template('edit_post.html', post=post)