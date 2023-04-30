"""Routes for user authentication."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from app import login_manager
from app.signup.signup_form import SignupForm
from app.signup.signup_models import User, db

# Blueprint Configuration
signup_blueprints = Blueprint("signup_blueprints", __name__, template_folder="templates", static_folder="static")


@signup_blueprints.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data, email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("home_blueprints.home"))
        flash("A user already exists with that email address.")
    return render_template(
        "signup.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("login_blueprints.login"))

