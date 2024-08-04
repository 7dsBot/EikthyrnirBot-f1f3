class WindowCapture:
    def __init__(self, window_title):
        import pygetwindow as gw
        import mss

        self.window_title = window_title
        self.window = gw.getWindowsWithTitle(window_title)[0]
        self.sct = mss.mss()

    def capture(self, capture_name=None, region=None):
        import mss.tools

        left, top, right, bottom = self.window.left, self.window.top, self.window.right, self.window.bottom
        if region is None:
            region = {"top": top, "left": left, "width": right - left, "height": bottom - top}
        screenshot = self.sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"{capture_name or self.window_title}.png")
        # print(f"Capture de la fenêtre '{self.window_title}' sauvegardée sous '{capture_name or self.window_title}.png'.")
