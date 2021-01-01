from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from project import db
from project.models import User, BlogPost
from project.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from project.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash("Thank you for your registration.", category="success")

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)

            next = request.args.get("next")

            if next == None or next[0] != "/":
                return redirect(url_for("core.index"))

            return redirect(next)
        else:
            flash("Invalid credentials.", category="danger")

    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("core.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        db.session.commit()
        flash("User profile updated successfully.", category="success")

        return redirect(url_for("users.account"))

    form.username.data = current_user.username
    form.email.data = current_user.email
    profile_image = url_for("static",
                            filename="profile_pics/" + current_user.profile_image)

    return render_template("account.html", profile_image=profile_image,
                           form=form)


@users.route("/<username>")
def user_posts(username: str):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(BlogPost.date.desc()).paginate(page=page,
                                                               per_page=5)
    # posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template("user_blog_posts.html", posts=posts, user=user)
