import os
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from bloglite import db
from bloglite.models import Post
from bloglite.posts.forms import PostForm
from werkzeug.utils import secure_filename

posts = Blueprint('posts', __name__)
upload_path = os.path.join('static', 'post_pics')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.image.data != None:
                file = form.image.data
                securefilename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, securefilename))

                post = Post(title=form.title.data,
                            content=form.content.data,
                            image=securefilename,
                            author=current_user)
                db.session.add(post)
                db.session.commit()
                flash('Your post has been created!', 'success')
                return redirect(url_for('main.home'))
            else:
                post = Post(title=form.title.data,
                            content=form.content.data,
                            author=current_user)
                db.session.add(post)
                db.session.commit()
                flash('Your post has been created!', 'success')
                return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
