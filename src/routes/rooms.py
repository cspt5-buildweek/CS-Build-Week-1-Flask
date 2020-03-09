from flask import request
from flask_restful import Resource

from models import db
from models.room import RoomsModel, RoomsSchema

room_schema = RoomsSchema()
rooms_schema = RoomsSchema(many=True)


class RoomsListResource(Resource):
    def get(self):
        rooms = RoomsModel.query.order_by(RoomsModel.id).all()
        return rooms_schema.dump(rooms)

    def post(self):
        new_room = RoomsModel(
            name=request.json['name'],
            description=request.json['description']
        )
        db.session.add(new_room)
        db.session.commit()
        return room_schema.dump(new_room)


class RoomResource(Resource):
    def get(self, room_id):
        room = RoomsModel.query.get_or_404(room_id)
        return room_schema.dump(room)

    def patch(self, room_id):
        room = RoomsModel.query.get_or_404(room_id)

        if 'name' in request.json:
            room.name = request.json['name']

        if 'description' in request.json:
            room.description = request.json['description']

        db.session.commit()
        return room_schema.dump(room)

    def delete(self, room_id):
        room = RoomsModel.query.get_or_404(room_id)
        db.session.delete(room)
        db.session.commit()
        return '', 204
