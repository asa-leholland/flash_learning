import os
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_user, current_user, logout_user,login_required
from flash_learning.models.student import Student
from flash_learning.main.forms import LoginForm,SignupForm, ResetForm
from flash_learning import db
from base64 import b64encode
from werkzeug.urls import url_parse



main = Blueprint("main", __name__)

@main.route('/', methods=["GET", "POST"])
def index():
    """The app's landing page."""
    return render_template("index.html")

@main.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset():
    """"Student login page."""
    if current_user.is_authenticated==False:
        return redirect(url_for("main.index"))
    form = ResetForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash("old password is invalid")
            return render_template("reset.html", title="reset password", form=form,current_user=current_user)

        if current_user.check_password(form.password.data)==current_user.check_password(form.new_password.data):
            flash("Password Can not be the same")
            return render_template("reset.html", title="reset password", form=form,current_user=current_user)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password Changed")
        return render_template("index.html")

    return render_template("reset.html", title="reset password", form=form,current_user=current_user)
    print(form.validate_on_submit)










@main.route('/login', methods=["GET", "POST"])
def login():
    """"Student login page."""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    # Redirect the student to their home page if username and password are correct, otherwise stay at the login page.
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("main.login"))
        if request.form.get('remember')!=None:
            login_user(user,remember=True)
        else:
            session.permanent = True
            login_user(user)
        return redirect(url_for("student.home", username=user.username))

    return render_template("login.html", title="Sign In", form=form)

"""Creates route for 404 error page"""
@main.app_errorhandler(404)
def handle_404(err):
    return render_template("error.html", title="Flash Learning Error Page", error_code=404), 404

"""Creates route for 500 error page"""
@main.app_errorhandler(500)
def handle_500(err):
    return render_template("error.html", title="Flash Learning Error Page", error_code=500), 500

# Add route to About page on main site
@main.route('/about', methods=["GET", "POST"])
def about():
    """The app's about page."""
    return render_template("about.html")


# Add route to FAQ page on main site
@main.route('/faq', methods=["GET", "POST"])
def faq():
    """The app's FAQ page."""
    return render_template("faq.html")

# Add route to main page on main site via a logout
@main.route("/logout")
def logout():
    """Logout the current user."""

    # Use Flask's base log out function to log out the user (manages sessions)
    logout_user()

    # Flash the log out message
    flash(f"You have been logged out!", "info")

    return redirect(url_for("main.index"))


# @main.route('/signup', methods=['POST','GET'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for("main.index"))
#
#     form = SignupForm()
#     if form.validate_on_submit():
#         user = Student(first_name=form.first_name.data,
#                        last_name=form.last_name.data,
#                        username=form.username.data,
#                        grade=form.grade.data,
#                        email=form.email.data,
#                        password=form.password.data)
#         alternative_id = b64encode(os.urandom(24)).decode('utf-8')
#         while Student.query.filter_by(alternative_id=alternative_id).first()!=None:
#             alternative_id = b64encode(os.urandom(24)).decode('utf-8')
#         user.set_password(form.password.data)
#         user.alternative_id=alternative_id
#         login_user(user, remember=False)
#         token = create_confirmation_token(user.email)
#         token="localhost:5000/confirm/"+token
#         db.session.add(user)
#         db.session.commit()
#         flash("Welcome to Flash Learning!")
#         flash(token)
#         return redirect(url_for("main.login"))
#     return render_template("signup.html", title="Sign Up", form=form)
#
#
#
# @main.route('/confirm/<token>', methods=['POST','GET'])
# def confirm_email(token):
#     try:
#         email = confirm_token(token)
#     except:
#         flash('This Confirmation Email has expired')
#         return redirect(url_for('main.index'))
#     user = Student.query.filter_by(email=email).first()
#     if user.activated:
#         flash('Account already confirmed. Please login.', 'success')
#     else:
#         user.activated = True
#         db.session.add(user)
#         db.session.commit()
#         flash('You have confirmed your account. Thanks!', 'success')
#     return redirect(url_for('main.index'))
#
