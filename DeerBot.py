from Floors.FloorOne import FloorOne
from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

from time import sleep

class DeerBot:
    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.wclick = WindowClicker("7DS")

    def define_team(self):
        # Cliquer sur le bouton "Définir l'équipe"
        self.wclick.click(964, 1042, 2)

        # Cliquer sur le bouton "Enregistrer"
        self.wclick.click(960, 910, 2)

        # Cliquer sur le bouton "OK"
        self.wclick.click(1060, 700, 2)

        # Prendre une capture d'écran de la fenêtre
        self.wcap.capture("team_set")
        print("Équipe définie.")

    def do_floor_one(self):
        floor_one = FloorOne()
        floor_one.enter_level()

        floor_one.run()

    def run(self):
        self.define_team()
        sleep(5)

        self.do_floor_one()