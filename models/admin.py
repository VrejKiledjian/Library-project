from hashlib import sha256
from flask_login import UserMixin
from peewee import CharField, DoesNotExist

from config import AppConfig
from .db import database


class Admin(database.Model, UserMixin):
    full_name_admin = CharField()
    password = CharField()
    email = CharField()
    roll = CharField(null=True)

    @staticmethod
    def hash_password(full_name, password):
        salt = AppConfig.SALT_KEY
        salted_password = f"{salt}.{full_name}:{password}.{salt}"
        hash_password = sha256(salted_password.encode())
        return hash_password.hexdigest()

    @classmethod
    def from_admin_registration_form(cls, form):
        return cls(
            full_name_admin=form.full_name_admin.data,
            password=cls.hash_password(form.full_name_admin.data, form.password.data),
            email=form.email.data,
            roll=form.roll.data,
        )

