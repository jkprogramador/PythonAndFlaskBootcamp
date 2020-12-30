from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """
    Class representing a record in table "users".
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    username = db.Column(db.String(100), unique=True, index=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password=password,
                                                    method="pbkdf2:sha256",
                                                    salt_length=8)

    def check_password(self, password: str):
        return check_password_hash(pwhash=self.password_hash,
                                   password=password)
