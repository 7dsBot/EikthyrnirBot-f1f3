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
            print("On est à l'étape 1.")
            return 1
        else:
            print("On n'est pas à l'étape 1.")
            return 0

    def run(self):
        while True:
            step = self.check_step()
            needs_color_cyle = step % 2 == 0

            if step == 1:
                hc = HandChecker()
                hand = hc.get_hand()
                card_colors = hc.get_colors_from_hand(hand)
                print(card_colors)
                pass

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