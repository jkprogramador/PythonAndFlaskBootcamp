import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# os.urandom(16)
app.config["SECRET_KEY"] = b'\x95\xac$*\x9a\xa0{\xdd\xa8\x16\xeb(\x15\x10\xabB'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,
                                                                    "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from myproject.puppies.views import puppies_blueprint
from myproject.owners.views import owners_blueprint

app.register_blueprint(puppies_blueprint, url_prefix="/puppies")
app.register_blueprint(owners_blueprint, url_prefix="/owners")
