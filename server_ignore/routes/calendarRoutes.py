from ..config import api
from .calendarRoutes import Calendars, CalendarsById

# calendar routes
api.add_resource(Calendars, "/calendars")
api.add_resource(CalendarsById, "/calendars/<int:calendar_id>")
