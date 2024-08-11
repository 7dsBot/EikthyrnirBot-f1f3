from Floors.FloorOne import FloorOne
from Floors.FloorTwo import FloorTwo
from WindowCapture import WindowCapture
from WindowClicker import WindowClicker

class DeerBot:
    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.wclick = WindowClicker("7DS")

    def define_team(self):
        DEFINE_TEAM_BUTTON = (964, 1042)
        self.wclick.click(*DEFINE_TEAM_BUTTON, 3)

        SAVE_BUTTON = (960, 910)
        self.wclick.click(*SAVE_BUTTON, 3)

        OK_BUTTON = (1060, 700)
        self.wclick.click(*OK_BUTTON, 3)

        print("Équipe définie.")

    def reset(self):
        RESET_TEAM_BUTTON = (960, 1040)
        self.wclick.click(*RESET_TEAM_BUTTON, 3)

        OK_BUTTON = (1060, 630)
        self.wclick.click(*OK_BUTTON, 3)

        print("Équipe réinitialisée.")

    def do_floor_one(self):
        floor_one = FloorOne()
        floor_one.enter_level()

        floor_one.run()

    def do_floor_two(self):
        floor_two = FloorTwo()
        floor_two.enter_level()

        floor_two.run()

    def run(self):
        while True:
            self.define_team()
            self.do_floor_one()
            self.do_floor_two()
            self.reset()
