from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddPuppyForm, DeletePuppyForm, AddOwnerForm
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# os.urandom(16)
app.config["SECRET_KEY"] = b'\x95\xac$*\x9a\xa0{\xdd\xa8\x16\xeb(\x15\x10\xabB'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,
                                                                    "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Puppy(db.Model):
    """
    Class representing a record in table "puppies".
    """
    __tablename__ = "puppies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    owner = db.relationship("Owner", backref="puppy",
                            uselist=False)  # one-to-one

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner name is {self.owner.name}."
        else:
            return f"Puppy name is {self.name} and is not assigned an owner yet."


class Owner(db.Model):
    """
    Class representing a record in table "owners".
    """
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppies.id"))

    def __init__(self, name: str, puppy_id: int):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        return f"Owner {self.name}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_puppy():
    form = AddPuppyForm()

    if form.validate_on_submit():
        name = form.name.data
        new_puppy = Puppy(name=name)
        db.session.add(new_puppy)
        db.session.commit()

        return redirect(url_for("list_puppies"))

    return render_template("add.html", form=form)


@app.route("/list")
def list_puppies():
    puppies = Puppy.query.all()

    return render_template("list.html", puppies=puppies)


@app.route("/delete", methods=["GET", "POST"])
def delete_puppy():
    form = DeletePuppyForm()

    if form.validate_on_submit():
        id = form.id.data
        puppy = Puppy.query.get(id)
        db.session.delete(puppy)
        db.session.commit()

        return redirect(url_for("list_puppies"))

    return render_template("delete.html", form=form)


@app.route("/add-owner", methods=["GET", "POST"])
def add_owner():
    form = AddOwnerForm()

    if form.validate_on_submit():
        owner_name = form.name.data
        puppy_id = form.puppy_id.data
        owner = Owner(name=owner_name, puppy_id=puppy_id)
        db.session.add(owner)
        db.session.commit()

        return redirect(url_for("list_puppies"))

    return render_template("add_owner.html", form=form)


if "__main__" == __name__:
    app.run(debug=True)
