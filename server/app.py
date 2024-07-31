from config import app, api

# user controller imports
from user_controllers import Signup, Login, CheckAuth, Logout

# calendar controller imports
from calendar_controllers import (
    CalendarQueryCreateController,
    CalendarPatchController,
    CalendarDeleteController,
)

# Event controller imports
from event_controllers import (
    EventQueryController,
    EventCreateController,
    EventPatchController,
    EventDeleteController,
    GuestEventQueryController,
    GuestEventCreateController,
    GuestEventPatchDeleteController,
)

# Task controller imports
from task_controllers import (
    TaskQueryController,
    TaskCreateController,
    TaskPatchController,
    TaskDeleteController,
    GuestTaskCreateController,
    GuestTaskPatchDeleteController,
)

# Invite controller imports
from invite_controllers import (
    SentInviteQueryController,
    InviteCreateController,
    InvitePatchController,
    InviteDeleteController,
)

# Colaboration controller imports
from collaboration_controllers import (
    CollaborationController,
    CollaborationPatchController,
    CollaborationDeleteController,
    GuestCollaborationQueryController,
    GuestCollaborationDeleteController,
)

api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckAuth, "/check_auth")

api.add_resource(CalendarQueryCreateController, "/calendars")
api.add_resource(CalendarPatchController, "/calendars/patch")
api.add_resource(
    CalendarDeleteController, "/calendars/delete/<string:calendar_string_id>"
)

api.add_resource(EventQueryController, "/events/query")
api.add_resource(EventCreateController, "/events/create")
api.add_resource(EventPatchController, "/events/patch")
api.add_resource(EventDeleteController, "/events/delete/<string:event_string_id>")
api.add_resource(GuestEventQueryController, "/guest_events/query")
api.add_resource(GuestEventCreateController, "/guest_events/create")
api.add_resource(GuestEventPatchDeleteController, "/guest_events")

api.add_resource(TaskQueryController, "/tasks/query")
api.add_resource(TaskCreateController, "/tasks/create")
api.add_resource(TaskPatchController, "/tasks/patch")
api.add_resource(TaskDeleteController, "/tasks/delete/<string:task_string_id>")
api.add_resource(GuestTaskCreateController, "/guest_tasks/create")
api.add_resource(GuestTaskPatchDeleteController, "/guest_tasks")

api.add_resource(SentInviteQueryController, "/invites/query/sent")
api.add_resource(InviteCreateController, "/invites/create")
api.add_resource(InvitePatchController, "/invites/patch")
api.add_resource(InviteDeleteController, "/invites/delete/<string:invite_string_id>")

api.add_resource(CollaborationController, "/collaborations")
api.add_resource(CollaborationPatchController, "/collaborations/patch")
api.add_resource(
    CollaborationDeleteController,
    "/collabortions/delete/<string:collaboration_string_id>",
)
api.add_resource(GuestCollaborationQueryController, "/guest_collaborations/query")
api.add_resource(
    GuestCollaborationDeleteController,
    "/guest_collaborations/delete/<string:collaboration_string_id>",
)


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
