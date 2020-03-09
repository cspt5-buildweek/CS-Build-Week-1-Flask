from models import db, ma


class RoomsModel(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Room {{ 'name': {self.name}, 'description': {self.description} }}>"


class RoomsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description")
        ordered = True
