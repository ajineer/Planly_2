from server.config import app, api
from server.controllers.usersController import Signup, Login, CheckSession, Logout


@app.route("/")
def index():
    return "<h1>Server Home</h1>"


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
