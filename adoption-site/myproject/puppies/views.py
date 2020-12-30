from flask import Blueprint, render_template, redirect, url_for
from myproject import db
from myproject.models import Puppy
from myproject.puppies.forms import AddForm, DeleteForm
from flask_login import login_required

puppies_blueprint = Blueprint("puppies", __name__,
                              template_folder="templates/puppies")


@puppies_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        new_puppy = Puppy(name=name)
        db.session.add(new_puppy)
        db.session.commit()

        return redirect(url_for("puppies.list"))

    return render_template("add.html", form=form)


@puppies_blueprint.route("/list")
def list():
    puppies = Puppy.query.all()

    return render_template("list.html", puppies=puppies)


@puppies_blueprint.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        puppy = Puppy.query.get(id)
        db.session.delete(puppy)
        db.session.commit()

        return redirect(url_for("puppies.list"))

    return render_template("delete.html", form=form)
