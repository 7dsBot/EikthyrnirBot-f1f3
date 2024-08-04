from PIL import Image

class ColorChecker:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def get_pixel_color(self, x, y):
        return self.image.getpixel((x, y))

    def check_pixel_color(self, x, y, expected_color, tolerance=0):
        pixel_color = self.get_pixel_color(x, y)
        return all(abs(pixel_color[i] - expected_color[i]) <= tolerance for i in range(3))
