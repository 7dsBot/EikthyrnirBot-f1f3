from pywinauto import Application
from pywinauto.mouse import press, release
from time import sleep
from WindowCapture import WindowCapture

class WindowClicker:
    def __init__(self, window_title):
        self.window_title = window_title
        self.app = Application().connect(title_re=window_title)
        self.window = self.app.window(title_re=window_title)

    def click(self, x, y, cooldown=0, hold_duration=0.05, button='left'):
        self._bring_window_to_foreground()
        abs_x, abs_y = self._calculate_absolute_coordinates(x, y)

        wcap = WindowCapture(self.window_title)

        while True:
            # Vérification pour le Hawk au milieu de l'écran
            if self._is_desired_pixel_color(wcap, (960, 520), (255, 255, 255), 10):
                sleep(0.5)
                continue

            self._perform_click(abs_x, abs_y, hold_duration, button)

            if cooldown:
                sleep(cooldown)

            break

    def _bring_window_to_foreground(self):
        self.window.restore()
        self.window.set_focus()

    def _calculate_absolute_coordinates(self, x, y):
        rect = self.window.rectangle()
        abs_x = rect.left + x
        abs_y = rect.top + y
        return abs_x, abs_y

    def _is_desired_pixel_color(self, wcap, coords, color, tolerance):
        return wcap.check_pixel_color(coords[0], coords[1], color, tolerance)

    def _perform_click(self, x, y, hold_duration, button):
        press(button=button, coords=(x, y))
        sleep(hold_duration)
        release(button=button, coords=(x, y))

