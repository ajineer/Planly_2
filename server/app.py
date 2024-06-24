from .config import app

# from controllers.usersController import Signup, Login, Logout, CheckSession
# from controllers.calendarsController import Calendars, CalendarsById
# from controllers.eventsController import Events, EventsById
# from controllers.tasksController import Tasks, TasksById
# from controllers.invitesController import Invite
# from controllers.participantsController import Particpants, ParticpantsById

# api.add_resource(Signup, "/signup")
# api.add_resource(Login, "/login")
# api.add_resource(CheckSession, "/check_session")
# api.add_resource(Logout, "/logout")
# api.add_resource(Tasks, "/tasks")
# api.add_resource(TasksById, "/task/<int:task_id>")
# api.add_resource(Invite, "/invites")
# api.add_resource(Events, "/events")
# api.add_resource(EventsById, "/events/<int:event_id>")
# api.add_resource(Calendars, "/calendars")
# api.add_resource(CalendarsById, "/calendars/<int:calendar_id>")

@app.route("/")
def index():
    return "<h1>Server Home</h1>"

if __name__ == "__main__":
    app.run(port=5555, debug=True)