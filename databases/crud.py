from main import db, Puppy, Owner, Toy

# Create
p1 = Puppy(name="Rufus", age=5, breed="Lab")
p2 = Puppy(name="Manoela", age=5, breed="Yorkshire")
db.session.add_all([p1, p2])
db.session.commit()

print(Puppy.query.all())

# Read
# all_puppies = Puppy.query.all()
# print(all_puppies)

# puppy_one = Puppy.query.get(1)
# print(puppy_one.name)
#
# frankie = Puppy.query.filter_by(name="Franky")
# print(frankie.all())

rufus = Puppy.query.filter_by(name="Rufus").first()
owner = Owner(name="Jose", puppy_id=rufus.id)
t1 = Toy(item_name="Chew toy", puppy_id=rufus.id)
t2 = Toy(item_name="Ball", puppy_id=rufus.id)
db.session.add_all([owner, t1, t2])
db.session.commit()

# Update
# puppy_one = Puppy.query.get(1)
# puppy_one.age = 7
# db.session.commit()

# Delete
# puppy_two = Puppy.query.get(2)
# db.session.delete(Puppy.query.all())
# db.session.commit()

# for p in Puppy.query.all():
#     db.session.delete(p)
#     db.session.commit()

# all_of_them = Puppy.query.all()
# print(all_of_them)
