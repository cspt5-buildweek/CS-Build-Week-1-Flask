from models import db
from models import ma
from models.node import NodesSchema


class LinksModel(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer(), db.ForeignKey('nodes.id'), nullable=False)
    target_id = db.Column(db.Integer(), db.ForeignKey('nodes.id'), nullable=False)
    source = db.relationship('NodesModel', foreign_keys=[source_id])
    target = db.relationship('NodesModel', foreign_keys=[target_id])
    source_direction = db.Column(db.String(), nullable=False)
    target_direction = db.Column(db.String(), nullable=False)

    def __init__(self, source_id, target_id, source_direction, target_direction):
        self.source_id = source_id
        self.target_id = target_id
        self.source_direction = source_direction
        self.target_direction = target_direction

    def __repr__(self):
        return f"<Link {{ " \
               f"'source_id': {self.source_id}, " \
               f"'target_id': {self.target_id}, " \
               f"'source_direction': {self.source_direction}, " \
               f"'target_direction': {self.target_direction} " \
               f"}}>"


class LinksSchema(ma.Schema):
    class Meta:
        fields = ("id", "source", "target", "source_direction", "target_direction")
        ordered = True
        include_fk = True

    source = ma.Nested(NodesSchema)
    target = ma.Nested(NodesSchema)
