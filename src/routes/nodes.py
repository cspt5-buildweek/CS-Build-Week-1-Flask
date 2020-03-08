from flask import request
from flask_restful import Resource

from models import db
from models.node import NodesModel, NodesSchema

node_schema = NodesSchema()
nodes_schema = NodesSchema(many=True)


class NodesListResource(Resource):
    def get(self):
        nodes = NodesModel.query.order_by(NodesModel.id).all()
        return {
            "Data": nodes_schema.dump(nodes)
        }

    def post(self):
        new_node = NodesModel(
            name=request.json['name'],
            description=request.json['description']
        )
        db.session.add(new_node)
        db.session.commit()
        return node_schema.dump(new_node)
