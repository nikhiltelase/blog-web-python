from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import date
from db import db, BlogPost, Comment
from forms import CreatePostForm, CommentForm

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = reversed(result.scalars().all())
    return render_template("index.html", all_posts=posts, user=current_user, flash=flash)


@blog_bp.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    # handle comments form
    form = CommentForm()
    focus_on = False
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text=form.comment.data,
                author=current_user,
                post=requested_post
            )
            db.session.add(new_comment)
            db.session.commit()
            focus_on = True
            flash('comment add successfully.', 'success')
            form.comment.data = ""  # Clear the field

        else:
            focus_on = True
            flash('please login first', 'error')

    comments = reversed(requested_post.comments)
    return render_template(
        "post.html",
        post=requested_post,
        comments=comments,
        form=form,
        focus_on=focus_on,
        user=current_user
    )


@blog_bp.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blog_bp.get_all_posts"))
    return render_template(
        "make-post.html",
        form=form,
        user=current_user)


@blog_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    if post.author_id != current_user.id:
        return "You do not have access to edit this post."
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("blog_bp.show_post", post_id=post.id))
    return render_template(
        "make-post.html",
        form=edit_form,
        is_edit=True,
        user=current_user
    )


@blog_bp.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    if post_to_delete.author_id != current_user.id:
        return "You do not have access to delete this post."
    comments = post_to_delete.comments
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('blog_bp.get_all_posts'))


@blog_bp.route('/about')
def about():
    return render_template("about.html", user=current_user)




