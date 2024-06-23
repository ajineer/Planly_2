from ..config import api
from .userRoutes import Signup, Login, CheckSession, Logout

# user routes
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")
