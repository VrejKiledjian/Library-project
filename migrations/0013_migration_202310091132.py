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
    borrowed_book = CharField(default=[], max_length=255)
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


def forward(old_orm, new_orm):
    old_student = old_orm['student']
    student = new_orm['student']
    return [
        # Convert datatype of the field student.borrowed_book: TEXT -> VARCHAR(255),
        student.update({student.borrowed_book: old_student.borrowed_book.cast('VARCHAR')}).where(old_student.borrowed_book.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_student = old_orm['student']
    student = new_orm['student']
    return [
        # Don't know how to do the conversion correctly, use the naive,
        student.update({student.borrowed_book: old_student.borrowed_book}).where(old_student.borrowed_book.is_null(False)),
    ]
