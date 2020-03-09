class Items:
    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

class Clothing(Items):
    def __init__(self, title, description, price, clothing_type, protection=0):
        super().__init__(title, description, price)
        self.clothing_type = clothing_type
        self.protection = protection

class Weapon(Items):
    def __init__(self, title, description, price, weapon_type, damage=0):
        super().__init__(title, description, price)
        self.weapon_type = weapon_type
        self.damage = damage