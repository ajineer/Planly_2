from config import app, api
from controllers import (
    Signup,
    Login,
    CalendarQueryCreateController,
    CalendarPatchController,
    CalendarDeleteController,
    EventQueryController,
    EventCreateController,
    GuestEventQueryController,
    GuestEventCreateController,
    GuestEventPatchDeleteController,
    TaskQueryController,
    TaskCreateController,
    TaskPatchController,
    TaskDeleteController,
    GuestTaskCreateController,
    GuestTaskPatchDeleteController,
    InviteQueryController,
    InviteCreateController,
    InvitePatchController,
    InviteDeleteController,
    CollaborationController,
    CollaborationPatchController,
    CollaborationDeleteController,
    GuestCollaborationQueryController
    GuestCollaborationDeleteController
)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")

api.add_resource(CalendarQueryCreateController, "/calendars", endpoint="calendars")
api.add_resource(CalendarPatchDeleteController, "/calendars<string:calendar_string_id>")

api.add_resource(EventQueryController, "/events/query", endpoint="query")
api.add_resource(EventCreateController, "/events/create", endpoint="create")
api.add_resource(EventPatchDeleteController, "/events/<string:event_string_id>")
api.add_resource(GuestEventControllerById, "/guest_events/<string:event_string_id>")

api.add_resource(GuestTaskController, "/guest_tasks/<string:collaboration_string_id>")
api.add_resource(GuestTaskControllerById, "/guest_tasks/<string:task_string_id>")


api.add_resource(InviteController, "/invites", endpoint="invites")
api.add_resource(InviteControllerById, "/invites/<string:invite_string_id>")

api.add_resource(CollaborationController, "/collaborations", endpoint="collaborations")
api.add_resource(
    GuestCollaborationController,
    "/guest_collaborations",
    endpoint="guest_collaborations",
)
api.add_resource(
    CollaborationControllerById, "/collaborations/<string:collaboration_string_id>"
)


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
