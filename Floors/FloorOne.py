from Card import CardType
from Floors.Floor import Floor

class FloorOne(Floor):
    def __init__(self):
        super().__init__()

    def enter_level(self):
        super().enter_level((970, 775), 1)

    def check_step(self):
        return super().check_step()

    def filter_cards_by_hero(self, cards):
        return super().filter_cards_by_hero(cards)

    def get_cards_to_play(self, hero_cards, last_color, step):
        color_cycle = ["red", "green", "blue"]
        needs_color_cyle = step % 2 == 0
        cards_to_play = []

        if needs_color_cyle:
            # On regarde si trois cartes "attack" ou "malus" de couleurs différentes sont disponibles
            are_there_three_colors = False
            colors = []

            for _, cards in hero_cards.items():
                for card in cards:
                    if card.type in ["attack", "malus"]:
                        if card.color not in colors:
                            colors.append(card.color)
                        if len(colors) >= 3:
                            are_there_three_colors = True
                            break
                if are_there_three_colors:
                    break

            # Si trois cartes "attack" ou "malus" de couleurs différentes sont disponibles, on prend une carte par couleur
            if are_there_three_colors:
                colors = []
                for _, cards in hero_cards.items():
                    for card in cards:
                        if card.type in ["attack", "malus"] and card.color not in colors:
                            cards_to_play.append(card)
                            colors.append(card.color)
                            break

                last_color_index = color_cycle.index(last_color)
                next_color_index = (last_color_index + 1) % 3
                next_color = color_cycle[next_color_index]

                cards_to_play = sorted(cards_to_play, key=lambda x: color_cycle.index(x.color) - next_color_index)

                if len(cards_to_play) < 4:
                    for _, cards in hero_cards.items():
                        for card in cards:
                            if (card.color == next_color and card not in cards_to_play) or (card.type == CardType.COUNTER and step != 2):
                                cards_to_play.append(card)
                                break
                        if len(cards_to_play) == 4:
                            break

            # Sinon on lance juste des cartes au pif
            else:
                for _, cards in hero_cards.items():
                    for card in cards:
                        cards_to_play.append(card)
                        if len(cards_to_play) == 4:
                            break
                    if len(cards_to_play) == 4:
                        break

            last_color = cards_to_play[-1].color

            cards_to_play = [card.index for card in cards_to_play]

        else:
            # On regarde si au minimum trois héros peuvent jouer une carte "attack" ou "malus"
            can_three_play = False
            count = 0

            for _, cards in hero_cards.items():
                for card in cards:
                    if card.type in ["attack", "malus"]:
                        count += 1
                        if count >= 3:
                            can_three_play = True
                            break
                if can_three_play:
                    break

            # Si trois héros peuvent jouer une carte "attack" ou "malus", on prend une carte par héros
            if can_three_play:
                for _, cards in hero_cards.items():
                    for card in cards:
                        if card.type in ["attack", "malus"]:
                            cards_to_play.append(card)
                            break

            # Sinon on lance juste des cartes "attack" et "malus" au hasard
            else:
                for _, cards in hero_cards.items():
                    for card in cards:
                        if card.type in ["attack", "malus"]:
                            cards_to_play.append(card)
                            if len(cards_to_play) == 4:
                                break
                    if len(cards_to_play) == 4:
                        break

            cards_to_play = [card.index for card in cards_to_play]

            # On complète par une quatrième carte "attack" ou "malus" si possible
            if len(cards_to_play) < 4:
                cards_left = [i for i in range(1, 9)]
                for card in cards_to_play:
                    cards_left.remove(card)
                cards_to_play.append(cards_left[0])

        while len(cards_to_play) < 4:
            cards_to_play.append(69)

        return cards_to_play, last_color

    def play_turn(self, cards):
        super().play_turn(cards)

    def play(self, step, cards, last_color="blue"):
        return super().play(step, cards, last_color)

    def run(self):
        super().run()
