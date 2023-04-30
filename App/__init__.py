"""Initialize app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import join_room, leave_room, send, SocketIO

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        from .assets import compile_static_assets

        # Register Blueprints
        from app.home.home_blueprints import home_blueprints
        app.register_blueprint(home_blueprints)

        from app.login.login_blueprints import login_blueprints
        app.register_blueprint(login_blueprints)

        from app.signup.signup_blueprints import signup_blueprints
        app.register_blueprint(signup_blueprints)

        # Create Database Models
        db.create_all()
        db.session.commit()

        # Compile static assets
        # if app.config["FLASK_ENV"] == "development":
        #     compile_static_assets(app)

        return app


