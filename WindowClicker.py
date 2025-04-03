from WindowClickerApi import WindowClickerApi
from time import sleep

class WindowClicker:
    def __init__(self, window_title):
        self.window_capture = WindowClickerApi(window_title)

    def click(self, x, y, cooldown=0.5, double_click=True):
        self.window_capture.click(x, y)
        if double_click:
            self.window_capture.click(x, y)
        sleep(cooldown)