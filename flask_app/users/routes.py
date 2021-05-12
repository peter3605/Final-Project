from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime

from ..email import send_email
from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User
from ..token import generate_confirmation_token, confirm_token

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for("users.confirm_email", token=token, _external=True)
        confirm_template = render_template("confirm.html", confirm_url=confirm_url)
        send_email(user.email, "Confirm your email", confirm_template)

        login_user(user)
        flash("Confirmation email has been sent")
        return redirect(url_for("users.account"))
        # return render_template("account.html")

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("texts.index"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if current_user.confirmed is False:
        return redirect(url_for("users.unconfirmed"))
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )


@users.route("/confirm/<token>")
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
        user = User.objects(email=email).first()
        if user.confirmed is False:
            current_user.modify(confirmed=True)
            current_user.save()
    except:
        flash("Confirmation link is invalid")
    return redirect(url_for('users.account'))
    # return render_template("account.html")


@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('users.account')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')