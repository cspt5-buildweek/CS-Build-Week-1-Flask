from items import Items, Clothing, Weapon

class Store:
    def __init__(self, in_stock = [Clothing('tunic', 'long sleeved', 10, 'shirt', 10), Clothing('leggings', 'additional protection from the weather', 5, 'pants', 15), Weapon('sword', 'pretty sharp, but could be sharper', 15, 'sword', 20)])
    self.in_stock = in_stock