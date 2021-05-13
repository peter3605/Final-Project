from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User, Text


# used to search for a text
class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


# used to enter new text
class TextForm(FlaskForm):
    name = StringField(
        "name", validators=[InputRequired(), Length(min=1, max=100)]
    )
    text = TextAreaField(
        "text", validators=[InputRequired(), Length(min=1, max=5000)]
    )
    submit = SubmitField("Save Text")

    # def validate_name(self, name):
    #     user = User.objects(username=current_user.username).first()
    #     texts = Text.objects(user=user, name=name).first()
    #     print(texts.name)
    #     if texts is not None:
    #         raise ValidationError("Title is taken")


# used to update text
class UpdateTextForm(FlaskForm):
    new_text = TextAreaField(
        "new_text", validators=[InputRequired(), Length(min=1, max=5000)]
    )
    submit = SubmitField("Save Text")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

    def validate_password(self, password):
        has_capital = False
        has_special_char = False
        special_chars = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
        for ch in password.data:
            if ch.isupper():
                has_capital = True
            if ch in special_chars:
                has_special_char = True
        if not has_capital:
            raise ValidationError("No capital letter in password")
        if not has_special_char:
            raise ValidationError("No special character in password")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")
