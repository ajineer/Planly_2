from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import secrets
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.secret_key = secrets.token_hex(16)
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
db = SQLAlchemy(metadata=metadata)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    from .models.User import User
    from .models.Participant import particpants
    from .models.Calendar import Calendar
    from .models.Invite import Invite
    from .models.Task import Task
    from .models.Event import Event

    db.create_all()
