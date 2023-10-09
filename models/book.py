from peewee import CharField, IntegerField, BigIntegerField, ForeignKeyField, TextField, DateField, BooleanField

from .student import Student
from .db import database


class Books(database.Model):
    title = CharField()
    author = CharField()
    publish_year = IntegerField()
    ISBN = BigIntegerField()
    image_path = CharField()
    summary = TextField()


class BooksCopy(database.Model):
    book = ForeignKeyField(Books, backref='copies')
    copy_number = CharField()
    is_available = BooleanField(default=True)
    title = CharField()

    # def reserve(self):
    #     if self.status == "Free":
    #         self.status = "Busy"
    #         self.save()
    #         return True
    #     else:
    #         return False
    #
    # def reserve_back(self):
    #     if self.status == "Busy":
    #         self.status = "Free"
    #         self.save()
    #         return True
    #     else:
    #         return False


class BorrowedBook(database.Model):
    student = ForeignKeyField(Student, backref='borrowed_books')
    book_copy = ForeignKeyField(BooksCopy, backref='borrowed_by_student')
    borrow_date = DateField()
    return_date = DateField(null=True)
