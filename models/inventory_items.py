from models import db

player_inventory = db.Table('inventory_items',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True),
    db.Column('items_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
)