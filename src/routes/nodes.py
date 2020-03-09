from flask import request
from flask_restful import Resource

from models import db
from models.node import NodesModel, NodesSchema

node_schema = NodesSchema()
nodes_schema = NodesSchema(many=True)


class NodesListResource(Resource):
    def get(self):
        nodes = NodesModel.query.order_by(NodesModel.id).all()
        return nodes_schema.dump(nodes)

    def post(self):
        new_node = NodesModel(
            room_id=request.json['room_id']
        )
        db.session.add(new_node)
        db.session.commit()
        return node_schema.dump(new_node)


class NodeResource(Resource):
    def get(self, node_id):
        node = NodesModel.query.get_or_404(node_id)
        return node_schema.dump(node)

    def patch(self, node_id):
        node = NodesModel.query.get_or_404(node_id)

        if 'room_id' in request.json:
            node.room_id = request.json['room_id']

        db.session.commit()
        return node_schema.dump(node)

    def delete(self, node_id):
        node = NodesModel.query.get_or_404(node_id)
        db.session.delete(node)
        db.session.commit()
        return '', 204
