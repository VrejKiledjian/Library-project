from .db import database
from peewee import CharField, IntegerField, DateTimeField


class Posts(database.Model):
    title = CharField(255)
    author = CharField(255)
    publish_year = IntegerField()
    ISBN = IntegerField()
    date_posted = DateTimeField()
    slug = CharField(255)
