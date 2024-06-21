from ..config import api
from .eventRoutes import Events, EventsById

# event routes
api.add_resource(Events, "/events")
api.add_resource(EventsById, "/events/<int:event_id>")
