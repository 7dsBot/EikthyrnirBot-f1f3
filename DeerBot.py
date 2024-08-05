from ColorChecker import ColorChecker
from HandChecker import HandChecker
from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

from time import sleep

wcap = WindowCapture("7DS")
wclick = WindowClicker("7DS")

class FloorOne:
    def __init__(self):
        pass

    def enter_level(self):
        # Cliquer sur l'étage 1
        wclick.click(970, 775, 1)

        # Cliquer sur le bouton "En avant !"
        wclick.click(960, 1020, 1)

        # TODO: Vérifier si on a assez d'endurance pour lancer le combat
        print("Étage 1 lancé.")

    def check_step(self):
        # Prendre une capture d'écran de la fenêtre
        wcap.capture("f1_step")

        # Regarder la couleur correspondant à l'étape
        cc = ColorChecker("f1_step.png")
        if cc.check_pixel_color(115, 70, (5, 101, 34), 10):
            return 1
        elif cc.check_pixel_color(115, 70, (22, 59, 110), 10):
            return 2
        elif cc.check_pixel_color(115, 70, (64, 4, 90), 10):
            return 3
        elif cc.check_pixel_color(115, 70, (110, 0, 48), 10):
            return 4
        else:
            raise Exception("Étape non reconnue.")

    def play(self, step, sorted_cards, last_color="blue"):
        color_cycle = ["red", "green", "blue"]
        needs_color_cyle = step % 2 == 0

        if needs_color_cyle:
            print("On a besoin d'un cycle de couleurs.")
            # On regarde si trois cartes "attack" ou "malus" de couleurs différentes sont disponibles
            are_there_three_colors = False
            colors = []
            for hero, attributes in sorted_cards.items():
                color, cards = attributes["color"], attributes["cards"]
                for card in cards:
                    if card["type"] in ["attack", "malus"]:
                        if color not in colors:
                            colors.append(color)
                        if len(colors) >= 3:
                            are_there_three_colors = True
                            break
                if are_there_three_colors:
                    break

            cards_to_play = []

            # Si trois cartes "attack" ou "malus" de couleurs différentes sont disponibles, on prend une carte par couleur
            if are_there_three_colors:
                colors = []
                for hero, attributes in sorted_cards.items():
                    color, cards = attributes["color"], attributes["cards"]
                    for card in cards:
                        if card["type"] in ["attack", "malus"] and color not in colors:
                            # rajouter l'attribut "color" à la carte
                            card["color"] = color
                            cards_to_play.append(card)
                            colors.append(color)
                            break
                print(f"Cartes à jouer: {cards_to_play}")
                # On regarde la dernière couleur jouée et on prend la prochaine carte dans le cycle (si last_color = "blue", on prend "red")
                last_color_index = color_cycle.index(last_color)
                next_color_index = (last_color_index + 1) % 3
                next_color = color_cycle[next_color_index]
                print(f"Dernière couleur jouée: {last_color}, prochaine couleur: {next_color}")

                # On ordonne les cartes à jouer dans l'ordre du cycle de couleurs en commençant par la couleur suivante
                cards_to_play = sorted(cards_to_play, key=lambda x: color_cycle.index(x["color"]) - next_color_index)

                # On complète par une quatrième carte dans le cycle ou par un contre
                if len(cards_to_play) < 4:
                    # On cherche d'abord une carte de la couleur next_color qui n'a pas encore été jouée
                    for hero, attributes in sorted_cards.items():
                        color, cards = attributes["color"], attributes["cards"]
                        for card in cards:
                            if (color == next_color and card not in cards_to_play) or (card["type"] == "counter" and step != 2):
                                cards_to_play.append(card)
                                break
                        if len(cards_to_play) == 4:
                            break

            # Sinon on lance juste des cartes au pif
            else:
                for hero, attributes in sorted_cards.items():
                    cards = attributes["cards"]
                    for card in cards:
                        cards_to_play.append(card)
                        if len(cards_to_play) == 4:
                            break

            last_color = cards_to_play[-1]["color"]

        else:
            print("On n'a pas besoin d'un cycle de couleurs.")
            # On regarde si au minimum trois héros peuvent jouer une carte "attack" ou "malus"
            can_three_play = False
            count = 0
            for hero, attributes in sorted_cards.items():
                color, cards = attributes["color"], attributes["cards"]
                for card in cards:
                    if card["type"] in ["attack", "malus"]:
                        count += 1
                        if count >= 3:
                            can_three_play = True
                            break
                if can_three_play:
                    break

            cards_to_play = []

            # Si trois héros peuvent jouer une carte "attack" ou "malus", on prend une carte par héros
            if can_three_play:
                for hero, attributes in sorted_cards.items():
                    color, cards = attributes["color"], attributes["cards"]
                    for card in cards:
                        if card["type"] in ["attack", "malus"]:
                            cards_to_play.append(card)
                            break

            # Sinon on lance juste des cartes "attack" et "malus" au hasard
            else:
                for hero, attributes in sorted_cards.items():
                    cards = attributes["cards"]
                    for card in cards:
                        if card["type"] in ["attack", "malus"]:
                            cards_to_play.append(card)

            # On complète par une quatrième carte "attack" ou "malus" si possible
            if len(cards_to_play) < 4:
                cards_left = [i for i in range(1, 8)]
                for card in cards_to_play:
                    cards_left.remove(card)
                cards_to_play.append(cards_left[0])

        cards_to_play = [card["index"] for card in cards_to_play]
        print(f"Cartes à jouer: {cards_to_play}")

        # On joue les cartes
        last_played = 0
        while len(cards_to_play) > 0:
            print(cards_to_play)
            card = cards_to_play[0]
            wclick.click(1230 + ((card - 1) * 86), 964, 1)
            last_played = card
            cards_to_play.remove(card)
            for i, card in enumerate(cards_to_play):
                if card < last_played:
                    cards_to_play[i] += 1

        return last_color

    def run(self):
        last_color = "blue"
        while True:
            step = self.check_step()

            hc = HandChecker()
            hand = hc.get_hand()
            sorted_cards = hc.get_sorted_cards(hand)
            # hc.print_hand(sorted_cards)

            last_color = self.play(step, sorted_cards, last_color)

            break

class DeerBot:
    def __init__(self):
        pass

    def define_team(self):
        # Cliquer sur le bouton "Définir l'équipe"
        wclick.click(964, 1042, 1)

        # Cliquer sur le bouton "Enregistrer"
        wclick.click(960, 910, 1)

        # Cliquer sur le bouton "OK"
        wclick.click(1060, 700, 2)

        # Prendre une capture d'écran de la fenêtre
        wcap.capture("team_set")
        print("Équipe définie.")

    def do_floor_one(self):
        floor_one = FloorOne()
        # floor_one.enter_level()

        floor_one.run()

    def run(self):
        # self.define_team()
        # sleep(2)

        self.do_floor_one()