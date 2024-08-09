import os

from Hand.CardCreator import CardCreator
from Hand.HandRarityChecker import HandRarityChecker
from ImageManager import ImageManager
from WindowCapture import WindowCapture

from constants import CARD_REGIONS

class HandChecker:
    def __init__(self):
        self.wcap = WindowCapture("7DS")

    def get_filtered_cards(self):
        skills_array = self.get_hand()
        filtered_cards = []

        for index, skill in enumerate(skills_array):
            card = self._create_card_from_skill(skill, index + 1)
            filtered_cards.append(card)

        return filtered_cards

    def _create_card_from_skill(self, skill, index):
        attributes = skill.split("_")
        hero = attributes[0]
        card_name = attributes[1]
        sealed = len(attributes) == 4
        card_level = attributes[-1]

        card_creator = CardCreator(hero, card_name, card_level, sealed, index)
        return card_creator.create_card()

    def get_hand(self):
        self._capture_hand_regions()

        skills_array = self._compare_with_skills()
        hand_rarities = self._check_hand_rarity()

        for i in range(len(skills_array)):
            skills_array[i] = f"{skills_array[i]}_{hand_rarities[i]}"

        return skills_array

    def _capture_hand_regions(self):
        for index, region in enumerate(CARD_REGIONS):
            self.wcap.capture(f"Hand/screenshots/{index}", region)

    def _compare_with_skills(self):
        skills_folder = "Skills"
        skills = [skill for skill in os.listdir(skills_folder) if skill.endswith(".png")]
        skills_array = []
        image_manager = ImageManager()

        for i in range(len(CARD_REGIONS)):
            hand_image = f"Hand/screenshots/{i}.png"
            similarity_percentages = []
            for skill in skills:
                similarity_percentage = image_manager.get_similarity_percentage(hand_image, f"{skills_folder}/{skill}")
                similarity_percentages.append(similarity_percentage * 100)
            best_match_index = similarity_percentages.index(max(similarity_percentages))
            best_match_skill = skills[best_match_index].split(".")[0]

            skills_array.append(best_match_skill)

        return skills_array

    def _check_hand_rarity(self):
        rarity_checker = HandRarityChecker()
        return rarity_checker.get_each_skill_rarity()
