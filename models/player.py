from models.inventory import Inventory

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()