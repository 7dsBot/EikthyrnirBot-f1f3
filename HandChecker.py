from WindowCapture import WindowCapture
import numpy as np
from PIL import Image
import os

wc = WindowCapture("7DS")

class HandChecker:
    def __init__(self):
        self.regions = [
            {"top": 904, "left": 1272, "width": 10, "height": 120},
            {"top": 904, "left": 1358, "width": 10, "height": 120},
            {"top": 904, "left": 1444, "width": 10, "height": 120},
            {"top": 904, "left": 1530, "width": 10, "height": 120},
            {"top": 904, "left": 1616, "width": 10, "height": 120},
            {"top": 904, "left": 1702, "width": 10, "height": 120},
            {"top": 904, "left": 1788, "width": 10, "height": 120},
            {"top": 904, "left": 1874, "width": 10, "height": 120},
        ]

    def are_images_equal(self, img1_path, img2_path):
        # Charger les images
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        # Vérifier si les tailles des images sont différentes
        if img1.size != img2.size:
            return False

        # Convertir les images en tableaux numpy pour une comparaison efficace
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)

        # Comparer les deux tableaux
        return np.array_equal(np_img1, np_img2)

    def get_hand(self):
        # Prendre une capture de chaque région de la main
        for i, region in enumerate(self.regions):
            wc.capture(f"Hand/{i}", region)

        # Comparer chaque région avec les cartes de compétences
        skills_folder = "Skills"
        skills = os.listdir(skills_folder)
        # Virer ce qui n'est pas une image
        skills = [skill for skill in skills if skill.endswith(".png")]

        skills_array = []

        for i in range(len(self.regions)):
            for skill in skills:
                hand_str = f"Hand/{i}.png"
                skill_str = f"{skills_folder}/{skill}"
                if self.are_images_equal(hand_str, skill_str):
                    skills_array.append(skill.split(".")[0])
                    break
            else:
                raise Exception(f"Carte non reconnue pour la région {i}.")
                break

        return skills_array

    def get_colors_from_hand(self, skills_array):
        card_colors = {
            "Thor": {
                "color": "blue",
                "index": []
            },
            "Albedo": {
                "color": "blue",
                "index": []
            },
            "Jörmungand": {
                "color": "green",
                "index": []
            },
            "Freyr": {
                "color": "red",
                "index": []
            }
        }

        for i, skill in enumerate(skills_array):
            if skill.startswith("Thor_"):
                card_colors["Thor"]["index"].append(i)
            elif skill.startswith("Albedo_"):
                card_colors["Albedo"]["index"].append(i)
            elif skill.startswith("Jörmungand_"):
                card_colors["Jörmungand"]["index"].append(i)
            elif skill.startswith("Freyr_"):
                card_colors["Freyr"]["index"].append(i)
            else:
                raise Exception(f"Carte non reconnue dans la main: {skill}.")

        return card_colors
