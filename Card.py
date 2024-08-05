class CardType:
    ATTACK = "attack"
    MALUS = "malus"
    COUNTER = "counter"
    ULTIMATE = "ultimate"

class Card:
    def __init__(self, hero, color, type, index):
        self.hero = hero
        self.color = color
        self.type = type
        self.index = index

    def __str__(self):
        return f"{self.hero} ({self.color}): {self.type} ({self.index})"
