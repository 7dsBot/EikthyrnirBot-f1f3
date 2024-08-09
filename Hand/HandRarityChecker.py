from WindowCapture import WindowCapture
from PIL import Image

class HandRarityChecker:
    BRONZE_COLOR = (21, 17, 12)
    BRONZE_SEALED_COLOR = (9, 7, 5)
    SILVER_COLOR = (37, 30, 87)
    SILVER_SEALED_COLOR = (16, 13, 37)
    GOLD_COLOR = (24, 48, 48)
    GOLD_SEALED_COLOR = (10, 21, 21)
    ULTIMATE_COLOR = (175, 176, 229)
    ULTIMATE_SEALED_COLOR = (75, 76, 98)

    def __init__(self):
        self.wcap = WindowCapture("7DS")
        self.rarities = []

    def get_each_skill_rarity(self):
        img = self._capture_screen()
        pixel_pairs = [self._get_skill_pixel_pair(img, i) for i in range(8)]

        for i, pixel in enumerate(pixel_pairs):
            rarity = self._determine_rarity(pixel, i)
            self.rarities.append(rarity)

        return self.rarities

    def _capture_screen(self):
        self.wcap.capture("Hand/screenshots/Screen")
        return Image.open("Hand/screenshots/Screen.png")

    def _get_skill_pixel_pair(self, img, index):
        x_offset = 1265 + index * 86
        y_offset = 1045
        return (
            img.getpixel((x_offset, y_offset)),
            img.getpixel((x_offset - 15, y_offset - 10))
        )

    def _calculate_color_distance(self, pixel, reference_color):
        return sum(abs(pixel[i] - reference_color[i]) for i in range(3))

    def _determine_rarity(self, pixel_pair, region_index):
        rarities = {
            "bronze": self._calculate_color_distance(pixel_pair[0], self.BRONZE_COLOR),
            "bronze_sealed": self._calculate_color_distance(pixel_pair[0], self.BRONZE_SEALED_COLOR),
            "silver": self._calculate_color_distance(pixel_pair[0], self.SILVER_COLOR),
            "silver_sealed": self._calculate_color_distance(pixel_pair[0], self.SILVER_SEALED_COLOR),
            "gold": self._calculate_color_distance(pixel_pair[0], self.GOLD_COLOR),
            "gold_sealed": self._calculate_color_distance(pixel_pair[0], self.GOLD_SEALED_COLOR),
            "ultimate": self._calculate_color_distance(pixel_pair[1], self.ULTIMATE_COLOR),
            "ultimate_sealed": self._calculate_color_distance(pixel_pair[1], self.ULTIMATE_SEALED_COLOR),
        }

        if all(distance > 150 for distance in rarities.values()):
            raise ValueError(f"Qualité de carte non reconnue pour la région {region_index}.")

        return min(rarities, key=rarities.get)
