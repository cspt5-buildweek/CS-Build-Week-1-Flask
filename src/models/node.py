from models import db, ma
from models.room import RoomsSchema


class NodesModel(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('RoomsModel', backref=db.backref('nodes', lazy=True))

    def __init__(self, room_id):
        self.room_id = room_id

    def __repr__(self):
        return f"<Node {{ 'room': {self.room} }}>"


class NodesSchema(ma.Schema):
    class Meta:
        fields = ("id", "room")
        ordered = True

    room = ma.Nested(RoomsSchema)
