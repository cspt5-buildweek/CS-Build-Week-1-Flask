# from models import db

# class ItemsModel(db.Model):
#     __tablename__ = 'items'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(), nullable=False)
#     description = db.Column(db.String(), nullable=False)
#     price = db.Column(db.Integer, nullable=False)

#     def __init__(self, title, description, price):
#         self.title = title
#         self.description = description
#         self.price = price