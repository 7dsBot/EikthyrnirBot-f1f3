from Floors.CardOrderer import CardOrderer
from Hand.Hand import Hand

from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

from time import sleep

class Floor:
    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.wclick = WindowClicker("7DS")

    def enter_level(self, level_coords, level_nb=1):
        # Cliquer sur l'étage
        self.wclick.click(level_coords[0], level_coords[1], 1)

        # Cliquer sur le bouton "En avant !"
        self.wclick.click(960, 1020, 1)

        # TODO: Vérifier si on a assez d'endurance pour lancer le combat

        print(f"Entrée dans l'étage {level_nb}.")

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

    def play_turn(self, cards):
        while len(cards) > 0:
            card = cards.pop(0)

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
        last_color = None
        step, last_step = 0, 0

        while True:
            step = self.check_step()
            if step != last_step:
                last_color = None

            if step == 69:
                break

            hand = Hand()
            cards = hand.get_cards()

            last_color = self.play(step, cards, last_color)
            sleep(40)

        self.wclick.click(1000, 1000, 1)
        sleep(10)
