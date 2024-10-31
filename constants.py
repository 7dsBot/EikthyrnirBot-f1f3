from dotenv import load_dotenv
from os import getenv

from Card import CardLevel, CardType

load_dotenv()
AHK_EXE_LOCATION = getenv("AHK_EXE_LOCATION")
AHK_SCRIPT_LOCATION = getenv("AHK_SCRIPT_LOCATION")

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

CARD_REGIONS = [{"top": 974, "left": 1232 + i * 86, "width": 50, "height": 50} for i in range(8)]

COLOR_CYCLE = [ "blue", "red", "green" ]

DEFINE_TEAM_BUTTON = (964, 1042)
SAVE_BUTTON = (960, 910)
SAVE_OK_BUTTON = (1060, 700)

RESET_TEAM_BUTTON = (960, 1040)
RESET_OK_BUTTON = (1060, 630)
