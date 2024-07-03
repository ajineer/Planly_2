from config import app, api
from controllers import (
    Signup,
    Login,
    Logout,
    CheckSession,
    CalendarController,
    CalendarControllerById,
    EventController,
    EventControllerById,
    TaskController,
    TaskControllerById,
    InviteController,
    InviteControllerById,
)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(CalendarController, "/calendars", endpoint="calendars")
api.add_resource(CalendarControllerById, "/calendars/<int:calendar_id>")
api.add_resource(InviteController, "/invites", endpoint="invites")
api.add_resource(InviteControllerById, "/invites/<int:invite_id>")
api.add_resource(TaskController, "/tasks", endpoint="tasks")
api.add_resource(TaskControllerById, "/task/<int:task_id>")
api.add_resource(EventController, "/events", endpoint="events")
api.add_resource(EventControllerById, "/events/<int:event_id>")


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
