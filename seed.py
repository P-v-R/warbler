"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import User, Message, Follows, Like

db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()

admin1 = User.signup(username = "admin1", email="g@g.com", password="admin1", image_url="")

db.session.add(admin1)
db.session.commit()

# breakpoint()
# like1 = Like(liking_user_id=301, message_liked_id=222)

# db.session.add(like1)
# db.session.commit()

