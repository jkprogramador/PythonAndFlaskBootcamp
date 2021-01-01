from flask import Blueprint, render_template, url_for, flash, redirect, \
    request, abort
from flask_login import login_user, current_user, logout_user, login_required
from project import db
from project.models import BlogPost
from project.blog_posts.forms import BlogPostForm

blog_posts = Blueprint("blog_posts", __name__)


@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        blog = BlogPost(title=title, content=content, user_id=current_user.id)
        db.session.add(blog)
        db.session.commit()
        flash("Blog Post created.", category="success")

        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form)


@blog_posts.route("/<int:blog_post_id>")
def read_blog_post(blog_post_id: int):
    post = BlogPost.query.get_or_404(blog_post_id)

    return render_template("blog_post.html", post=post)


@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(blog_post_id: int):
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Blog Post Updated.", category="success")

        return redirect(
            url_for("blog_posts.read_blog_post", blog_post_id=post.id))

    form.title.data = post.title
    form.content.data = post.content

    return render_template("create_post.html", title="Update Blog Post",
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=["POST"])
@login_required
def delete_post(blog_post_id: int):
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Blog Post Removed.", category="success")

    return redirect(url_for("core.index"))
