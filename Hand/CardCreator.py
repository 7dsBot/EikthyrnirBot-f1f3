from Card import Card

from constants import HERO_CONFIG, LEVEL_CONFIG

class CardCreator:
    def __init__(self, hero, card_name, card_level, sealed, index):
        self.hero = hero
        self.card_name = card_name
        self.card_level = card_level
        self.sealed = sealed
        self.index = index

    def create_card(self):
        self._validate_hero_and_card()
        hero_config = HERO_CONFIG[self.hero]
        color = hero_config["color"]
        card_type = hero_config["cards"][self.card_name]

        return Card(self.hero, color, self.card_name, card_type, self.index, LEVEL_CONFIG[self.card_level], self.sealed)

    def _validate_hero_and_card(self):
        if self.hero not in HERO_CONFIG:
            raise ValueError(f"Héros non reconnu: {self.hero}.")
        if self.card_name not in HERO_CONFIG[self.hero]["cards"]:
            raise ValueError(f"Carte non reconnue pour {self.hero}: {self.card_name}.")
