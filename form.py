from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, EmailField, IntegerField, SubmitField, FileField
from wtforms.validators import InputRequired, NumberRange, EqualTo, Optional, Email


class CreateUserForm(FlaskForm):
    full_name = StringField(
        validators=[
            InputRequired(),
        ],
    )
    grade = DecimalField(
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100),
        ],
    )
    password = StringField(
        validators=[
            InputRequired(),
        ]
    )
    repeat_password = StringField(
        validators=[
            EqualTo(
                "password",
                message="Passwords don't match",
            ),
        ]
    )


class AddBookForm(FlaskForm):
    title = StringField(
        validators=[
            InputRequired()
        ]
    )
    author = StringField(
        validators=[
            InputRequired()
        ]
    )
    publish_year = IntegerField(
        validators=[
            InputRequired()
        ]
    )
    ISBN = IntegerField(
        "ISBN",
        validators=[
            InputRequired()
        ]
    )
    summary = StringField(
        validators=[
            Optional()
        ]
    )
    image_path = StringField(
        validators=[
            InputRequired()
        ]
    )


# class DelBookForm(FlaskForm):
#     ID = IntegerField(
#         validators=[
#             InputRequired()
#         ]
#     )
#     title = StringField(
#         validators=[
#             InputRequired()
#         ]
#     )


class SearchForm(FlaskForm):
    searched = StringField(
        "Searched",
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    full_name = StringField(
        validators=[
            InputRequired(),
        ],
    )
    password = StringField(
        validators=[
            InputRequired(),
        ],
    )


class AdminForm(FlaskForm):
    full_name_admin = StringField(
        validators=[
            InputRequired(),
        ],
    )
    roll = StringField(
        validators=[
            InputRequired()
        ]
    )
    email = EmailField(
        validators=[
            InputRequired(),
            Email()
        ]
    )
    password = StringField(
        validators=[
            InputRequired(),
        ]
    )
    repeat_password = StringField(
        validators=[
            EqualTo(
                "password",
                message="Passwords don't match",
            ),
        ]
    )


class AdminLoginForm(FlaskForm):
    full_name_admin = StringField(
        validators=[
            InputRequired()
        ]
    )
    password = StringField(
        validators=[
            InputRequired()
        ]
    )
    email = EmailField(
        validators=[
            Email(),
            InputRequired()
        ]
    )

# class RegisterForm(FlaskForm):
#     password = StringField(
#         validators=[
#             InputRequired(),
#         ]
#     )
#     repeat_password = StringField(
#         validators=[
#             EqualTo(
#                 "password",
#                 message="Passwords don't match",
#             ),
#         ]
#     )
#     full_name = StringField(
#         validators=[
#             InputRequired(),
#         ]
#     )
#     grade = IntegerField(
#         validators=[
#             InputRequired()
#         ]
#     )
