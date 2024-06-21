from .config import app, api
from .controllers.usersController import Signup, Login, CheckSession, Logout
from .controllers.calendarsController import Calendars, CalendarsById
from .controllers.eventsController import Events, EventsById
from .controllers.tasksController import Tasks, TasksById
from .controllers.invitesController import Invite


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


# user routes
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")

# invite routes
api.add_resource(Invite, "/invites")


# calendar routes
api.add_resource(Calendars, "/calendars")
api.add_resource(CalendarsById, "/calendars/<int:calendar_id>")

# event routes
api.add_resource(Events, "/events")
api.add_resource(EventsById, "/events/<int:event_id>")

# task routes
api.add_resource(Tasks, "/tasks")
api.add_resource(TasksById, "/task/<int:task_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
