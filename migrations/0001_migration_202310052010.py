# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Student(peewee.Model):
    full_name = CharField(max_length=60)
    grade = IntegerField()
    password = CharField(max_length=255)
    book_limit = IntegerField(default=5)
    borrowed_book = TextField(null=True)
    roll = CharField(max_length=255, null=True)
    class Meta:
        table_name = "student"


