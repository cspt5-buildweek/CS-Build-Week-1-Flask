from models import db

player_inventory = db.Table('inventory_items',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True),
    db.Column('items_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
)

class InventoryModel(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship("items", secondary=player_inventory, backref=db.backref('items_in_inventory', lazy='dynamic'))

    # def __init__(self, user_id, items):
    #     self.user_id = user_id
    #     self.items = items

class ItemsModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    # def __init__(self, title, description, price):
    #     self.title = title
    #     self.description = description
    #     self.price = price

# inv = InventoryModel()
# item = ItemsModel()
# inv.items.append(item)
# db.session.add(inv)
# db.session.commit()
