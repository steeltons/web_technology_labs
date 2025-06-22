from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///structure.db'

db.init_app(app)

cors = CORS(app, supports_credentials= True, resources= {r"/api/*": {"origins": 'http://localhost:3000'}})