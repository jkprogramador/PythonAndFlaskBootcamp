from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config[
    "SECRET_KEY"] = b'\x04\xce^\xec\xcaZ\xfd\x89C\xbe\x8c\x8e\xe3s\\\x1e'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,
                                                                    "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

api = Api(app)

jwt = JWT(app=app, authentication_handler=authenticate,
          identity_handler=identity)


# class HelloWorld(Resource):
#
#     def get(self):
#         return {"message": "Hello World!"}


# api.add_resource(HelloWorld, "/")

class Puppy(db.Model):
    __tablename__ = "puppies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name}


class PuppyNames(Resource):
    @jwt_required()
    def get(self, name: str):
        puppy = Puppy.query.filter_by(name=name).first()

        if puppy:
            return puppy.json()

        return {"id": None, "name": None}, 404

    def post(self, name: str):
        puppy = Puppy(name=name)
        db.session.add(puppy)
        db.session.commit()

        return puppy.json()

    @jwt_required()
    def delete(self, name: str):
        puppy = Puppy.query.filter_by(name=name).first()
        db.session.delete(puppy)
        db.session.commit()

        return {"success": True}


class AllNames(Resource):
    def get(self):
        return [puppy.json() for puppy in Puppy.query.all()]


api.add_resource(PuppyNames, "/puppy/<string:name>")
api.add_resource(AllNames, "/puppies")

if "__main__" == __name__:
    app.run(debug=True)
