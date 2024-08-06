class CardLevel:
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    ULTIMATE = "ultimate"

class CardType:
    ATTACK = "attack"
    MALUS = "malus"
    COUNTER = "counter"
    ULTIMATE = "ultimate"

class Card:
    def __init__(self, hero, color, card_name, card_type, index, level, sealed=False):
        self.hero = hero
        self.color = color
        self.name = card_name
        self.type = card_type
        self.index = index
        self.level = level
        self.sealed = sealed

    def __str__(self):
        return f"{self.hero} ({self.color}) Card(\'name\': {self.name}, \'type\': {self.type}, \'index\': {self.index}, \'level\': {self.level}, \'sealed\': {self.sealed})"

    def upgrade(self):
        if self.level == CardLevel.BRONZE:
            self.level = CardLevel.SILVER
        elif self.level == CardLevel.SILVER:
            self.level = CardLevel.GOLD

        return self
