from Hand.HandChecker import HandChecker

class Hand:
    def __init__(self):
        self.cards = []
        self.hc = HandChecker()

    def __str__(self):
        return "Hand:\n" + "\n".join([str(card) for card in self.cards])

    def get_cards(self):
        self.cards = self.hc.get_filtered_cards()

        return self.cards
