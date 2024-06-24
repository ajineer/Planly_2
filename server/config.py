from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
import secrets

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

app = Flask(__name__, instance_path='/Users/ajineer/Desktop/Development/code/phase-6/Planly_2/server/instance')
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt(app)
api = Api()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False
app.secret_key = secrets.token_hex(16)

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app)