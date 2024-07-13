from config import app, api
from controllers import (
    Signup,
    Login,
    Logout,
    CheckSession,
    CalendarController,
    CalendarControllerById,
    GuestCalendarControllerById,
    EventController,
    EventControllerById,
    GuestEventController,
    GuestEventControllerById,
    TaskController,
    TaskControllerById,
    GuestTaskController,
    GuestTaskControllerById,
    InviteController,
    InviteControllerById,
    CollaborationController,
)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")

api.add_resource(CalendarController, "/calendars", endpoint="calendars")
api.add_resource(CalendarControllerById, "/calendars/<string:calendar_string_id>")
api.add_resource(
    GuestCalendarControllerById, "/guest_calendars/<string:calendar_string_id>"
)


api.add_resource(TaskController, "/tasks", endpoint="tasks")
api.add_resource(TaskControllerById, "/tasks/<string:task_string_id>")
api.add_resource(GuestTaskController, "/guest_tasks/<string:task_string_id>")
api.add_resource(GuestTaskControllerById, "/guest_tasks/<string:task_string_id>")

api.add_resource(EventController, "/events", endpoint="events")
api.add_resource(EventControllerById, "/events/<string:event_string_id>")
api.add_resource(GuestEventController, "/guest_events/<string:event_string_id>")
api.add_resource(GuestEventControllerById, "/guest_events/<string:event_string_id>")

api.add_resource(InviteController, "/invites", endpoint="invites")
api.add_resource(InviteControllerById, "/invites/<string:invite_string_id>")

api.add_resource(CollaborationController, "/collaborations", endpoint="collaborations")


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
