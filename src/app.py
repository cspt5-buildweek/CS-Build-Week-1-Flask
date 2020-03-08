import util

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from models import db, ma
from routes.nodes import NodesListResource

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = util.get_db_connect_string()

db.init_app(app)
ma.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(NodesListResource, '/nodes')
