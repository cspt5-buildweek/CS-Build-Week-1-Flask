from models import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    starting_room = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    inventory = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    coin_pouch = db.Column(db.Integer, default=0)
    auth_key = db.Column(db.String())

    def __init__(self, username, password, auth_key):
        self.username = username
        self.password = password
        self.auth_key = auth_key
        # self.starting_room = starting_room
        # self.inventory = inventory
        # self.coin_pouch = coin_pouch

    def __repr__(self):
        return f"<User {{ 'username': {self.username}, 'password': {self.password} }}>"
