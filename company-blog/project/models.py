from project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime as dt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """
    Class representing a record in table "users".
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(100), nullable=False,
                              default="default_profile.png")
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    username = db.Column(db.String(100), nullable=False, unique=True,
                         index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    posts = db.relationship("BlogPost", backref="author", lazy="dynamic")

    def __init__(self, email: str, username: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password=password,
                                                    method="pbkdf2:sha256",
                                                    salt_length=8)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.username}:{self.id}"


class BlogPost(db.Model):
    """
    Class representing a record in table "blog_posts".
    """
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, title: str, content: str, user_id: int):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Post {self.id}"
