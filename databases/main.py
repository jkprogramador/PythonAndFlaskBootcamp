import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,
                                                                    "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# set FLASK_APP=main.py
# flask db init
# flask db migrate -m "Message here."
# flask db upgrade
Migrate(app, db)


class Puppy(db.Model):
    """
    Class that represents a Puppy record in the puppies table.
    """
    __tablename__ = "puppies"  # Manual table name choice.

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    breed = db.Column(db.String(100), nullable=False)
    # One-to-many.
    toys = db.relationship("Toy", backref="puppy", lazy="dynamic")
    # One-to-one.
    owner = db.relationship("Owner", backref="puppy", uselist=False)

    def __init__(self, name: str, age: int, breed: str):
        self.name = name
        self.age = age
        self.breed = breed

    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner is {self.owner.name}."
        else:
            return f"Puppy name is {self.name} and has no owner."

    def report_toys(self):
        for toy in self.toys:
            print(toy.item_name)


class Owner(db.Model):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppies.id"))

    def __init__(self, name: str, puppy_id: int):
        self.name = name
        self.puppy_id = puppy_id


class Toy(db.Model):
    __tablename__ = "toys"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(250), nullable=False)
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppies.id"))

    def __init__(self, item_name: str, puppy_id: int):
        self.item_name = item_name
        self.puppy_id = puppy_id


if "__main__" == __name__:
    app.run(debug=True)
