from Card import CardLevel, CardType

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
