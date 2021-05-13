from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from ..forms import SearchForm, TextForm, UpdateTextForm
from ..models import User, Text
from ..utils import current_time

texts = Blueprint("texts", __name__)


@texts.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_anonymous is False and current_user.confirmed is False:
        return render_template('unconfirmed.html')
    form = SearchForm()
    form2 = TextForm()

    if form2.validate_on_submit() and current_user.is_authenticated:
        text = Text(
            user=current_user._get_current_object(),
            name=form2.name.data,
            text=form2.text.data,
            date=current_time()
        )
        text.save()

        return redirect(request.path)

    if current_user.is_authenticated:
        user = User.objects(username=current_user.username).first()
        texts = Text.objects(user=user)
        return render_template("index.html", form=form, form2=form2, texts=texts)

    # enable to display all stored texts for user on site
    return render_template("main.html")


@texts.route("/user/<username>")
def user_detail(username):
    if current_user.is_anonymous is False and current_user.confirmed is False:
        return render_template('unconfirmed.html')

    form = SearchForm()
    user = User.objects(username=username).first()
    texts = Text.objects(user=user)

    return render_template("user_detail.html", username=username, texts=texts, form=form)

@texts.route("/text/<title>") 
def update_text(title):
    form = UpdateTextForm()

    if form.validate_on_submit():
        print("redirect")
        new_text = form.new_text.data
        user = User.objects(username=current_user.username).first()
        texts = Text.objects(user=user, name=title)
        texts.modify(text=new_text)
        texts.save()
        return redirect(url_for("texts.index"))
        
    print("update")
    print(form.errors)
    return render_template("update.html", form=form)

