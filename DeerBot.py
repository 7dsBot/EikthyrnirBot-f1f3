from Floors.FloorOne import FloorOne
from Floors.FloorTwo import FloorTwo
from Floors.FloorThree import FloorThree
from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

from constants import DEFINE_TEAM_BUTTON, SAVE_BUTTON, SAVE_OK_BUTTON, RESET_TEAM_BUTTON, RESET_OK_BUTTON

class DeerBot:
    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.wclick = WindowClicker("7DS")

    def define_team(self):
        self.wclick.click(*DEFINE_TEAM_BUTTON, 3)
        self.wclick.click(*SAVE_BUTTON, 3)
        self.wclick.click(*SAVE_OK_BUTTON, 3)

        print("Équipe définie.")

    def reset(self):
        self.wclick.click(*RESET_TEAM_BUTTON, 3)
        self.wclick.click(*RESET_OK_BUTTON, 3)

        print("Équipe réinitialisée.")

    def do_floor_one(self):
        floor_one = FloorOne()
        floor_one.enter_level()

        floor_one.run()

        print("Étage 1 terminé.")

    def do_floor_two(self):
        floor_two = FloorTwo()
        floor_two.enter_level()

        floor_two.run()

        print("Étage 2 terminé.")

    def do_floor_three(self):
        floor_three = FloorThree()
        floor_three.enter_level()

        floor_three.run()

        print("Étage 3 terminé.")

    def run(self, *args):
        diffStart = 0
        if len(args) > 0:
            diffStart = int(args[0])
            if diffStart < 1 or diffStart > 3:
                print("Invalid difficulty level. Please enter a number between 1 and 3.")
                return

        counter = 1

        if diffStart == 3:
            print("Starting at floor 3")
            self.do_floor_three()
            self.reset()
        elif diffStart == 2:
            print("Starting at floor 2")
            self.do_floor_two()
            self.do_floor_three()
            self.reset()

        while True:
            print(f"\nRun #{counter}\n")
            self.define_team()
            self.do_floor_one()
            self.do_floor_two()
            self.do_floor_three()
            self.reset()
            counter += 1
