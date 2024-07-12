from config import app, api
from controllers import (
    Signup,
    Login,
    Logout,
    CheckSession,
    CalendarController,
    CalendarControllerById,
    EventController,
    TaskController,
    InviteController,
    GuestTaskController,
    CollaborationController,
)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(CalendarController, "/calendars", endpoint="calendars")
api.add_resource(CalendarControllerById, "/calendars/<int:calendar_id>")
api.add_resource(InviteController, "/invites", endpoint="invites")
api.add_resource(TaskController, "/tasks", endpoint="tasks")
api.add_resource(EventController, "/events", endpoint="events")
api.add_resource(GuestTaskController, "/guest_tasks", endpoint="guest_tasks")
api.add_resource(CollaborationController, "/collaborations", endpoint="collaborations")


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
