from Floors.FloorOne import FloorOne
from Floors.FloorTwo import FloorTwo
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

        # print("Équipe définie.")

    def reset(self):
        self.wclick.click(*RESET_TEAM_BUTTON, 3)
        self.wclick.click(*RESET_OK_BUTTON, 3)

        # print("Équipe réinitialisée.")

    def do_floor_one(self):
        floor_one = FloorOne()
        floor_one.enter_level()

        floor_one.run()

    def do_floor_two(self):
        floor_two = FloorTwo()
        floor_two.enter_level()

        floor_two.run()

    def run(self):
        # counter = 1
        while True:
            # print(f"Run #{counter}")
            self.define_team()
            self.do_floor_one()
            # self.do_floor_two()
            self.reset()
            # counter += 1
