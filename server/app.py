from config import app, api
from controllers import (
    Signup,
    Login,
    Logout,
    CheckSession,
    Calendars,
    CalendarsById,
    Events,
    EventsById,
    Tasks,
    TasksById,
    Invite,
    InvitesById,
)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Calendars, "/calendars", endpoint="calendars")
api.add_resource(CalendarsById, "/calendars/<int:calendar_id>")
api.add_resource(Invite, "/invites", endpoint="invites")
api.add_resource(InvitesById, "/invites/<int:invite_id>")
api.add_resource(Tasks, "/tasks")
api.add_resource(TasksById, "/task/<int:task_id>")
api.add_resource(Events, "/events")
api.add_resource(EventsById, "/events/<int:event_id>")


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
