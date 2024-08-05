from time import sleep

class WindowClicker:
    def __init__(self, window_title):
        from pywinauto import Application

        self.window_title = window_title
        self.app = Application().connect(title_re=window_title)
        self.window = self.app.window(title_re=window_title)

    def click(self, x, y, cooldown=0, hold_duration=0.05):
        from pywinauto.mouse import press, release
        from time import sleep

        self.window.restore()
        self.window.set_focus()
        rect = self.window.rectangle()
        abs_x, abs_y = rect.left + x, rect.top + y

        press(button='left', coords=(abs_x, abs_y))
        sleep(hold_duration)
        release(button='left', coords=(abs_x, abs_y))

        if cooldown:
            sleep(cooldown)
