from Card import CardType
from Floors.CardOrderer import CardOrderer
from Hand.Hand import Hand
from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

from time import sleep

class FloorOne:
    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.wclick = WindowClicker("7DS")

    def enter_level(self):
        # Cliquer sur l'étage 1
        self.wclick.click(970, 775, 1)

        # Cliquer sur le bouton "En avant !"
        self.wclick.click(960, 1020, 1)

        # TODO: Vérifier si on a assez d'endurance pour lancer le combat
        print("Étage 1 lancé.")

        # Passer l'animation d'entrée
        sleep(8)
        self.wclick.click(960, 540, 15, 0.05, 'right')

    def check_step(self):
        PHASE_1 = (5, 101, 34)
        PHASE_2 = (22, 59, 110)
        PHASE_3 = (64, 4, 90)
        PHASE_4 = (110, 0, 48)
        PHASES = [PHASE_1, PHASE_2, PHASE_3, PHASE_4]

        END = (76, 164, 124)

        for i, phase in enumerate(PHASES):
            if self.wcap.check_pixel_color(115, 70, phase, 10):
                return i + 1

        sleep(5)
        if self.wcap.check_pixel_color(1000, 1000, END, 10):
            return 69

        raise Exception("Étape non reconnue.")

    def filter_cards_by_hero(self, cards):
        hero_cards = {}
        for card in cards:
            if card.hero not in hero_cards:
                hero_cards[card.hero] = []
            hero_cards[card.hero].append(card)
        return hero_cards

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

    def play_turn(self, cards_to_play):
        while len(cards_to_play) > 0:
            card = cards_to_play.pop(0)

            # On clique sur la carte
            if card == 69:
                self.wclick.click(1075, 790, 1)
            else:
                self.wclick.click(1230 + ((card - 1) * 86), 964, 2)

        # On reclique en 10, 10 pour décaler la souris
        self.wclick.click(10, 10, 0)

    def play(self, step, cards, last_color="blue"):
        # On répartit les cartes à jouer parmi les héros
        hero_cards = self.filter_cards_by_hero(cards)

        # On récupère les cartes qu'on va jouer ce tour ainsi que la couleur de la dernière carte jouée si besoin
        cards_to_play, last_color = self.get_cards_to_play(hero_cards, last_color, step)

        # On doit regarder quand on joue une carte si les index des autres sont toujours valides
        cards_to_play = CardOrderer(cards_to_play, cards).order_card_indexes()

        # On joue le tour
        self.play_turn(cards_to_play)

        return last_color

    def run(self):
        last_color = "blue"

        while True:
            step = self.check_step()

            if step == 69:
                break

            hand = Hand()
            cards = hand.get_cards()

            last_color = self.play(step, cards, last_color)
            sleep(40)

        self.wclick.click(1000, 1000, 1)
        sleep(10)
