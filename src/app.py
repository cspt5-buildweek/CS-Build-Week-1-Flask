import util

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from models import db, ma
# import models for migrate to work
from models import link, node, room, inventory_items, user
from routes.nodes import NodesListResource, NodeResource
from routes.rooms import RoomsListResource, RoomResource
from routes.links import LinksListResource, LinksResource

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = util.get_db_connect_string()

db.init_app(app)
ma.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

# Rooms routes
api.add_resource(RoomsListResource, '/rooms')
api.add_resource(RoomResource, '/rooms/<int:room_id>')

# Nodes routes
api.add_resource(NodesListResource, '/nodes')
api.add_resource(NodeResource, '/nodes/<int:node_id>')

# Links routes
api.add_resource(LinksListResource, '/links')
api.add_resource(LinksResource, '/links/<int:link_id>')
