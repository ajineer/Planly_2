from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS
import secrets
import os
from . import config

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(directory=os.path.join(os.path.dirname(__file__), "migrations"))
bcrypt = Bcrypt()
api = Api()

from .controllers.usersController import Signup, Login, CheckSession, Logout
from .controllers.calendarsController import Calendars, CalendarsById
from .controllers.eventsController import Events, EventsById
from .controllers.tasksController import Tasks, TasksById
from .controllers.invitesController import Invite
from .controllers.participantsController import Particpants, ParticpantsById


def create_app():
    print("working")
    app = Flask(__name__)
    app.config.from_object(config)
    app.json.compact = False
    app.secret_key = secrets.token_hex(16)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api.init_app(app)
    CORS(app)

    @app.route("/")
    def index():
        return "<h1>Server Home</h1>"

    api.add_resource(Signup, "/signup")
    api.add_resource(Login, "/login")
    api.add_resource(CheckSession, "/check_session")
    api.add_resource(Logout, "/logout")
    api.add_resource(Tasks, "/tasks")
    api.add_resource(TasksById, "/task/<int:task_id>")
    api.add_resource(Invite, "/invites")
    api.add_resource(Events, "/events")
    api.add_resource(EventsById, "/events/<int:event_id>")
    api.add_resource(Calendars, "/calendars")
    api.add_resource(CalendarsById, "/calendars/<int:calendar_id>")

    return app
