from ..config import api
from .inviteRoutes import Invite

# invite routes
api.add_resource(Invite, "/invites")
