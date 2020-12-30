from myproject import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from is_safe_url import is_safe_url
from urllib.parse import urlparse


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration complete.")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out.")

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            next = request.args.get("next")

            if not is_safe_url(next, allowed_hosts={
                urlparse(request.host_url).netloc}):
                return abort(400)

            # if next == None or next[0] != "/":
            #     next = url_for("index")

            return redirect(next)
        else:
            flash("Invalid credentials.")

    return render_template("login.html", form=form)


if "__main__" == __name__:
    app.run(debug=True)
