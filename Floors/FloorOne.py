from Card import CardType
from Floors.Floor import Floor

from constants import COLOR_CYCLE

class TurnPlayer:
    @staticmethod
    def get_cards_to_play(hero_cards, last_color, step):
        steps = {
            1: TurnPlayer.step_1,
            2: TurnPlayer.step_2,
            3: TurnPlayer.step_3,
            4: TurnPlayer.step_4
        }

        if step not in steps:
            raise Exception("Étape non reconnue.")

        return steps[step](hero_cards, last_color)

    @staticmethod
    def step_1(hero_cards, last_color):
        cards_to_play = [7, 5, 3, 1]

        return cards_to_play, last_color

    @staticmethod
    def step_2(hero_cards, last_color):
        cards_to_play = [2, 3, 1, 4]

        return cards_to_play, last_color

    @staticmethod
    def step_3(hero_cards, last_color):
        cards_to_play = []

        if TurnPlayer._can_three_different_heroes_play(hero_cards):
            cards_to_play = TurnPlayer._play_priority_cards(hero_cards, check_color=False)
            cards_to_play = TurnPlayer._add_missing_cards(hero_cards, cards_to_play)
        else:
            cards_to_play = TurnPlayer._play_last_four_cards()

        cards_to_play = TurnPlayer._eventually_play_fourth_card(cards_to_play)
        cards_to_play = TurnPlayer._ensure_four_cards_are_played(cards_to_play)

        return cards_to_play, last_color

    @staticmethod
    def step_4(hero_cards, last_color):
        cards_to_play = []

        if TurnPlayer._are_there_three_colors_to_play(hero_cards):
            cards_to_play = TurnPlayer._play_priority_cards(hero_cards, check_color=True)
            cards_to_play = TurnPlayer._respect_color_cycle(cards_to_play, last_color)
            cards_to_play = TurnPlayer._complete_color_cycle(hero_cards, cards_to_play, 4)
            last_color = cards_to_play[-1].color
        else:
            cards_to_play = TurnPlayer._play_last_four_cards()
            last_color = None

        cards_to_play = TurnPlayer._get_index_array(cards_to_play)
        cards_to_play = TurnPlayer._ensure_four_cards_are_played(cards_to_play)

        return cards_to_play, last_color

    @staticmethod
    def _respect_color_cycle(cards_to_play, last_color):
        last_color_index = COLOR_CYCLE.index(last_color) if last_color in COLOR_CYCLE else 2
        next_color_index = (last_color_index + 1) % 3

        cards_to_play = sorted(cards_to_play, key=lambda x: COLOR_CYCLE.index(x.color) - next_color_index)

        return cards_to_play

    @staticmethod
    def _complete_color_cycle(hero_cards, cards_to_play, step):
        if len(cards_to_play) < 4:
            next_color = COLOR_CYCLE[(COLOR_CYCLE.index(cards_to_play[-1].color) + 1) % 3]

            for _, cards in hero_cards.items():
                for card in cards:
                    if (card.color == next_color and card not in cards_to_play) or (card.type == CardType.COUNTER and step != 2):
                        cards_to_play.append(card)
                        break
                if len(cards_to_play) == 4:
                    break

        return cards_to_play

    @staticmethod
    def _play_priority_cards(hero_cards, check_color=False):
        cards_to_play = []
        colors = []

        for _, cards in hero_cards.items():
            for card in cards:
                if check_color and card.type in ["attack", "malus", "ultimate"] and card.color not in colors:
                    cards_to_play.append(card)
                    colors.append(card.color)
                    break
                elif not check_color and card.type in ["attack", "malus", "ultimate"]:
                    cards_to_play.append(card)
                    break

            if len(cards_to_play) == 3:
                break

        return cards_to_play

    @staticmethod
    def _get_index_array(cards_to_play):
        return [card.index for card in cards_to_play]

    @staticmethod
    def _add_missing_cards(hero_cards, cards_to_play):
        if len(cards_to_play) < 3:
            cards_to_play = TurnPlayer._add_additional_priority_cards(hero_cards, cards_to_play)

        if len(cards_to_play) < 4:
            cards_to_play = TurnPlayer._add_counter_card(hero_cards, cards_to_play)

        return TurnPlayer._get_index_array(cards_to_play)

    @staticmethod
    def _eventually_play_fourth_card(cards_to_play):
        if len(cards_to_play) < 4:
            cards_left = [i for i in range(1, 8)]
            for index in cards_to_play:
                cards_left.remove(index)
            cards_to_play.append(cards_left[0])

        return cards_to_play

    @staticmethod
    def _add_additional_priority_cards(hero_cards, cards_to_play):
        for _, cards in hero_cards.items():
            for card in cards:
                if card.type in ["attack", "malus", "ultimate"] and card not in cards_to_play:
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 3:
                break
        return cards_to_play

    @staticmethod
    def _add_counter_card(hero_cards, cards_to_play):
        for _, cards in hero_cards.items():
            for card in cards:
                if card.type == CardType.COUNTER:
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 4:
                break
        return cards_to_play

    @staticmethod
    def _play_last_four_cards():
        return [8, 7, 6, 5]

    @staticmethod
    def _can_three_different_heroes_play(hero_cards):
        counter = 0

        for _, cards in hero_cards.items():
            for card in cards:
                if card.type in ["attack", "malus", "ultimate"]:
                    counter += 1
                    break

        return counter >= 3

    @staticmethod
    def _are_there_three_colors_to_play(hero_cards):
        colors = TurnPlayer._get_nb_of_cards_per_color(hero_cards)

        return all(color_nb > 0 for color_nb in colors.values())

    @staticmethod
    def _get_nb_of_cards_per_color(hero_cards):
        colors = {}

        for _, cards in hero_cards.items():
            for card in cards:
                if card.color not in colors:
                    colors[card.color] = 0
                colors[card.color] += 1

        return colors

    @staticmethod
    def _ensure_four_cards_are_played(cards_to_play):
        while len(cards_to_play) < 4:
            cards_to_play.append(69)

        return cards_to_play

class FloorOne(Floor):
    def __init__(self):
        super().__init__()

    def enter_level(self):
        super().enter_level((970, 775), 1)

    def check_step(self):
        return super().check_step()

    def filter_cards_by_hero(self, cards):
        return super().filter_cards_by_hero(cards)

    def get_cards_to_play(self, hero_cards, last_color, step, turn):
        return TurnPlayer.get_cards_to_play(hero_cards, last_color, step)

    def play_turn(self, cards):
        super().play_turn(cards)

    def play(self, step, cards, last_color, turn):
        return super().play(step, cards, last_color, turn)

    def run(self):
        super().run()
