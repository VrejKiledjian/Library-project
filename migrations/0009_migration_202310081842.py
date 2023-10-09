# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Admin(peewee.Model):
    full_name_admin = CharField(max_length=255)
    password = CharField(max_length=255)
    email = CharField(max_length=255)
    roll = CharField(max_length=255, null=True)
    class Meta:
        table_name = "admin"


@snapshot.append
class Books(peewee.Model):
    title = CharField(max_length=255)
    author = CharField(max_length=255)
    publish_year = IntegerField()
    ISBN = BigIntegerField()
    image_path = CharField(max_length=255)
    summary = TextField()
    class Meta:
        table_name = "books"


@snapshot.append
class BooksCopy(peewee.Model):
    book = snapshot.ForeignKeyField(backref='copies', index=True, model='books')
    copy_number = CharField(max_length=255)
    is_available = BooleanField(default=True)
    title = CharField(max_length=255)
    class Meta:
        table_name = "bookscopy"


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


@snapshot.append
class BorrowedBook(peewee.Model):
    student = snapshot.ForeignKeyField(backref='borrowed_books', index=True, model='student')
    book_copy = snapshot.ForeignKeyField(backref='borrowed_by_student', index=True, model='bookscopy')
    borrow_date = DateField()
    return_date = DateField(null=True)
    class Meta:
        table_name = "borrowedbook"


