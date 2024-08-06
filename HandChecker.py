from WindowCapture import WindowCapture
import numpy as np
from PIL import Image
import os
from Card import Card, CardLevel, CardType

class HandChecker:
    HERO_CONFIG = {
        "Thor": {"color": "blue", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}},
        "Albedo": {"color": "blue", "cards": {"1": CardType.MALUS, "2": CardType.COUNTER, "Ult": CardType.ULTIMATE}},
        "Jörmungand": {"color": "green", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}},
        "Freyr": {"color": "red", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}}
    }

    LEVEL_CONFIG = {
        "bronze": CardLevel.BRONZE,
        "silver": CardLevel.SILVER,
        "gold": CardLevel.GOLD,
        "ultimate": CardLevel.ULTIMATE,
        "bronze_sealed": CardLevel.BRONZE,
        "silver_sealed": CardLevel.SILVER,
        "gold_sealed": CardLevel.GOLD,
        "ultimate_sealed": CardLevel.ULTIMATE
    }

    def __init__(self):
        self.regions = [
            {"top": 974, "left": 1232, "width": 50, "height": 50},
            {"top": 974, "left": 1318, "width": 50, "height": 50},
            {"top": 974, "left": 1404, "width": 50, "height": 50},
            {"top": 974, "left": 1490, "width": 50, "height": 50},
            {"top": 974, "left": 1576, "width": 50, "height": 50},
            {"top": 974, "left": 1662, "width": 50, "height": 50},
            {"top": 974, "left": 1748, "width": 50, "height": 50},
            {"top": 974, "left": 1834, "width": 50, "height": 50},
        ]

        self.wcap = WindowCapture("7DS")

    def create_card(self, hero, card_name, card_level, sealed, index):
        if hero not in self.HERO_CONFIG:
            raise Exception(f"Héros non reconnu: {hero}.")

        hero_config = self.HERO_CONFIG[hero]
        if card_name not in hero_config["cards"]:
            raise Exception(f"Carte non reconnue pour {hero}: {card_name}.")

        card_type = hero_config["cards"][card_name]
        color = hero_config["color"]

        return Card(hero, color, card_name, card_type, index, self.LEVEL_CONFIG[card_level], sealed)

    def get_filtered_cards(self, skills_array):
        cards = []

        for i, skill in enumerate(skills_array):
            hero, card_name, sealed, card_level = None, None, False, None
            attributes = skill.split("_")

            if len(attributes) == 4:
                hero, card_name, sealed, card_level = attributes[0], attributes[1], True, attributes[3]
            else:
                hero, card_name, card_level = attributes

            card = self.create_card(hero, card_name, card_level, sealed, i + 1)
            cards.append(card)

        return cards

    def get_similarity_percentage(self, img1_path, img2_path):
        # Charger les images
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        # Vérifier si les tailles des images sont différentes
        if img1.size != img2.size:
            return False

        # Convertir les images en tableaux numpy pour une comparaison efficace
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)

        # On boucle sur chaque ligne puis chaque pixel de chaque ligne, et on fait une incertitude de 10
        good_pixels = 0
        for i in range(np_img1.shape[0]):
            for j in range(np_img1.shape[1]):
                for k in range(np_img1.shape[2]):
                    res = np_img1[i, j, k] - np_img2[i, j, k]
                    res = abs(res)
                    if res > 30:
                        pass
                    else:
                        good_pixels += 1

        # On calcule le pourcentage de pixels identiques
        percentage = good_pixels / (np_img1.shape[0] * np_img1.shape[1] * np_img1.shape[2])

        return percentage

    def get_each_skill_level(self, skills_array):
        # Capture the entire screen
        self.wcap.capture("Hand/Screen")

        pixel_pairs = []
        img = Image.open("Hand/Screen.png")

        for i in range(0, 8):
            pixel = (img.getpixel((1265 + i * 86, 1045)), img.getpixel((1250 + i * 86, 1035)))
            pixel_pairs.append(pixel)

        for i, pixel in enumerate(pixel_pairs):
            bronze = abs(pixel[0][0] - 21) + abs(pixel[0][1] - 17) + abs(pixel[0][2] - 12)
            bronze_sealed = abs(pixel[0][0] - 9) + abs(pixel[0][1] - 7) + abs(pixel[0][2] - 5)

            silver = abs(pixel[0][0] - 37) + abs(pixel[0][1] - 30) + abs(pixel[0][2] - 87)
            silver_sealed = abs(pixel[0][0] - 16) + abs(pixel[0][1] - 13) + abs(pixel[0][2] - 37)

            gold = abs(pixel[0][0] - 24) + abs(pixel[0][1] - 48) + abs(pixel[0][2] - 48)
            gold_sealed = abs(pixel[0][0] - 10) + abs(pixel[0][1] - 21) + abs(pixel[0][2] - 21)

            ultimate = abs(pixel[1][0] - 175) + abs(pixel[1][1] - 176) + abs(pixel[1][2] - 229)
            ultimate_sealed = abs(pixel[1][0] - 75) + abs(pixel[1][1] - 76) + abs(pixel[1][2] - 98)

            # print(f"Region {i}: bronze={bronze}, silver={silver}, gold={gold}, ultimate={ultimate}")
            # print(f"Sealed region {i}: bronze_sealed={bronze_sealed}, silver_sealed={silver_sealed}, gold_sealed={gold_sealed}, ultimate_sealed={ultimate_sealed}")

            rarities = {
                "bronze": bronze,
                "silver": silver,
                "gold": gold,
                "ultimate": ultimate,
                "bronze_sealed": bronze_sealed,
                "silver_sealed": silver_sealed,
                "gold_sealed": gold_sealed,
                "ultimate_sealed": ultimate_sealed
            }

            if all(value > 150 for value in rarities.values()):
                raise Exception(f"Qualité de carte non reconnue pour la région {i}.")

            # print(f"Valeurs enregistrées pour la région {i}: {rarities}")

            rarity = min(rarities, key=rarities.get)
            skills_array[i] = f"{skills_array[i]}_{rarity.split('_')[0]}"

        return skills_array

    def get_hand(self):
        # Prendre une capture de chaque région de la main
        for i, region in enumerate(self.regions):
            self.wcap.capture(f"Hand/{i}", region)

        # Comparer chaque région avec les cartes de compétences
        skills_folder = "Skills"
        skills = os.listdir(skills_folder)
        # Virer ce qui n'est pas une image
        skills = [skill for skill in skills if skill.endswith(".png")]

        skills_array = []

        for i in range(len(self.regions)):
            all_percentages = []
            for skill in skills:
                hand_str = f"Hand/{i}.png"
                skill_str = f"{skills_folder}/{skill}"
                percentage = self.get_similarity_percentage(hand_str, skill_str)
                all_percentages.append(round(percentage * 100, 2))

            # print(f"Pour la région {i}, les pourcentages sont: {all_percentages}")

            highest_percentage = max(all_percentages)
            highest_percentage_index = all_percentages.index(highest_percentage)
            corresponding_skill = skills[highest_percentage_index]
            skill_name = corresponding_skill.split(".")[0]

            # print(f"Pour la région {i}, la compétence reconnue est: {skill_name} avec un pourcentage de {highest_percentage}%")
            # print(f"La deuxième compétence la plus probable est: {skills[all_percentages.index(sorted(all_percentages, reverse=True)[1])]} avec un pourcentage de {sorted(all_percentages, reverse=True)[1]}%")
            # print(f"La moyenne des autres pourcentages est de: {round(sum(all_percentages) / len(all_percentages), 2)}%")

            skills_array.append(skill_name)

        hand = self.get_each_skill_level(skills_array)

        return hand

    def print_hand(self, cards):
        for card in cards:
            print(card)
