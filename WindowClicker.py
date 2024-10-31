import subprocess

from pywinauto import Application

from constants import AHK_EXE_LOCATION, AHK_SCRIPT_LOCATION

class WindowClicker:
    def __init__(self, window_title):
        self.window_title = window_title
        self.app = Application().connect(title_re=window_title)
        self.window = self.app.window(title_re=window_title)

    def click(self, x, y, cooldown=0, double_click=True):
        self._bring_window_to_foreground()
        abs_x, abs_y = self._calculate_absolute_coordinates(x, y)

        self._perform_click(abs_x, abs_y, cooldown, double_click)

    def _bring_window_to_foreground(self):
        self.window.restore()
        self.window.set_focus()

    def _calculate_absolute_coordinates(self, x, y):
        rect = self.window.rectangle()
        abs_x = rect.left + x
        abs_y = rect.top + y
        return abs_x, abs_y

    def _perform_click(self, x, y, cooldown, double_click):
        args = [str(x), str(y), str(cooldown), str(int(double_click))]
        command = [AHK_EXE_LOCATION, AHK_SCRIPT_LOCATION] + args
        subprocess.run(command)
