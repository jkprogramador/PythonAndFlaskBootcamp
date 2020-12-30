from myproject import db


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
