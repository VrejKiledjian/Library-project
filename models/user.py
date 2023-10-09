from hashlib import sha256

from peewee import CharField, IntegerField, TextField

from config import AppConfig
from .db import database


class User(database.Model):
    full_name = CharField(max_length=50)
    grade = IntegerField()
    password = CharField()
    book_limit = IntegerField(default=5)
    borrowed_book = TextField(null=True)
    user_from = CharField()

    @classmethod
    def from_registration_form(cls, form):
        return cls(
            username=form.username.data,
            full_name=form.full_name.data,
            password=cls.hash_password(form.username.data, form.password.data),
        )

    # @staticmethod
    #
    # def hash_password(username, password):
    #     salted_password = f"{AppConfig.SALT_KEY}.{username}:{password}.{AppConfig.SALT_KEY}"
    #     hash_generator = sha256(salted_password.encode())
    #     return hash_generator.hexdigest()