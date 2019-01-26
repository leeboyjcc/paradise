from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User
<<<<<<< HEAD
from flask_migrate import Migrate
from flask_login import LoginManager

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
=======

def register_blueprints(app):
    from .handlers import front, course, admin, user
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(user)
>>>>>>> 94eabd4a7886dac73ee0b413078e4000d94daeab

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
<<<<<<< HEAD
    register_extensions(app)
=======
    db.init_app(app)
>>>>>>> 94eabd4a7886dac73ee0b413078e4000d94daeab
    register_blueprints(app)

    return app

