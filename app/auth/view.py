from flask import flash, url_for, redirect, render_template, request, session
from . import auth
from .form import LoginForm, RegistrationForm
from ..model import Users, db, Model
from .. import login_manager
from flask_login import login_user, logout_user, login_required
from ..decorators import admin_required


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_name=request.form.get('email')).first()
        if user is not None and user.check_password(request.form.get('password')):
            login_user(user, remember=True)
            return redirect(url_for("auth.success"))
        else:
            flash("You entered incorrect email or password")
    return render_template("index.html", form=form, title="login")


@auth.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(request.form.get('email'), request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("auth.success"))
    return render_template("index.html", form=form, title="registration")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("auth.login"))


@auth.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("log_in.html", title="log in", permission="You are an Admin")


@auth.route("/success")
@login_required
def success():
    model = Model.query.all()
    return render_template("log_in.html", title="log in", permission="You are an Admin")


@auth.route("/")
def index():
    return render_template("base.html", title="log in")
