from hashlib import sha256
from config import AppConfig
from flask_login import UserMixin
from peewee import CharField, IntegerField, TextField, PrimaryKeyField
from .db import database


class Student(database.Model, UserMixin):
    full_name = CharField(max_length=60)
    grade = IntegerField()
    password = CharField()
    book_limit = IntegerField(default=5)
    borrowed_book = CharField(default="")
    roll = CharField(null=True)

    def get_id(self):
        return self.id

    @staticmethod
    def hash_password(full_name, password):
        salt = AppConfig.SALT_KEY
        salted_password = f"{salt}.{full_name}:{password}.{salt}"
        hashed_password = sha256(salted_password.encode())
        return hashed_password.hexdigest()

    @classmethod
    def from_student_add_form(cls, form):
        return cls(
            full_name=form.full_name.data,
            grade=form.grade.data,
            password=cls.hash_password(form.full_name.data, form.password.data),
        )

    @classmethod
    def from_registration_form(cls, form):
        return cls(
            full_name=form.full_name.data,
            grade=form.grade.data,
            password=cls.hash_password(form.full_name.data, form.password.data),
        )
