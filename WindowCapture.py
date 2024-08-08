import pygetwindow as gw
import mss
import mss.tools

class WindowCapture:
    RED, GREEN, BLUE = 0, 1, 2

    def __init__(self, window_title):
        self.window_title = window_title
        self.window = self._get_window_by_title(window_title)
        self.sct = mss.mss()

    def capture(self, capture_name=None, region=None):
        region = region or self._get_window_region()
        screenshot = self.sct.grab(region)
        self._save_screenshot(screenshot, capture_name or self.window_title)

    def check_pixel_color(self, x, y, expected_color, tolerance=0):
        screenshot = self.sct.grab(self._get_window_region())
        pixel_color = screenshot.pixel(x, y)
        return self._colors_are_within_tolerance(pixel_color, expected_color, tolerance)

    def _get_window_by_title(self, window_title):
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            raise ValueError(f"No window found with title: {window_title}")
        return windows[0]

    def _get_window_region(self):
        left, top, right, bottom = self.window.left, self.window.top, self.window.right, self.window.bottom
        return {"top": top, "left": left, "width": right - left, "height": bottom - top}

    def _save_screenshot(self, screenshot, filename):
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"{filename}.png")

    def _colors_are_within_tolerance(self, pixel_color, expected_color, tolerance):
        return all(abs(pixel_color[i] - expected_color[i]) <= tolerance for i in (self.RED, self.GREEN, self.BLUE))
