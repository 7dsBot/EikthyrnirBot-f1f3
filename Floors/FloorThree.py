from Card import CardType
from Floors.Floor import Floor

from constants import COLOR_CYCLE

from sys import exit

class TurnPlayer:
    @staticmethod
    def get_cards_to_play(hero_cards, last_color, step, turn):
        steps = {
            1: TurnPlayer.step_1,
            2: TurnPlayer.step_2,
            3: TurnPlayer.step_3,
            4: TurnPlayer.step_4
        }

        if step not in steps:
            raise Exception("Étape non reconnue.")

        return steps[step](hero_cards, last_color, turn)

    @staticmethod
    def step_1(hero_cards, last_color, turn):
        cards_to_play = [7, 5, 3, 1]

        return cards_to_play, last_color

    @staticmethod
    def step_2(hero_cards, last_color, turn):
        cards_to_play = []

        if turn == 1 and TurnPlayer._have_more_than_one_counter(hero_cards):
            cards_to_play = [2, 3, 1, 4]
            last_color = "red"
            return cards_to_play, last_color

        if TurnPlayer._are_there_three_colors_to_play(hero_cards):
            cards_to_play = TurnPlayer._play_priority_cards(hero_cards, check_color=True)
            cards_to_play = TurnPlayer._respect_color_cycle(cards_to_play, last_color)
            cards_to_play = TurnPlayer._complete_color_cycle(hero_cards, cards_to_play, 2, turn)
            last_color = cards_to_play[-1].color
        else:
            cards_to_play = TurnPlayer._play_last_four_cards()
            last_color = None

        cards_to_play = TurnPlayer._get_index_array(cards_to_play)
        cards_to_play = TurnPlayer._ensure_four_cards_are_played(cards_to_play)

        return cards_to_play, last_color

    @staticmethod
    def step_3(hero_cards, last_color, turn):
        cards_to_play = []

        # Here we don't care about the color cycle, but we need to keep at least one card of each color and a counter card
        cards_to_play = TurnPlayer._prepare_finish(hero_cards, last_color, turn)
        # set_trace()
        cards_to_play = TurnPlayer._get_index_array(cards_to_play)
        cards_to_play = TurnPlayer._ensure_four_cards_are_played(cards_to_play)

        return cards_to_play, last_color

    @staticmethod
    def step_4(hero_cards, last_color, turn):
        cards_to_play = []

        if turn == 1:
            # Specific case for step 4, need to play blue attack/malus/ultimate skill, then red, then green and NEED to play a counter card at the end
            cards_to_play = TurnPlayer._finish_him(hero_cards, last_color, turn)
            if len(cards_to_play) < 4:
                raise Exception("Finish him failed, restarting floor 3")
            cards_to_play = TurnPlayer._get_index_array(cards_to_play)
        else:
            if TurnPlayer._are_there_three_colors_to_play(hero_cards):
                cards_to_play = TurnPlayer._play_priority_cards(hero_cards, check_color=True)
                cards_to_play = TurnPlayer._respect_color_cycle(cards_to_play, last_color)
                cards_to_play = TurnPlayer._complete_color_cycle(hero_cards, cards_to_play, 4, turn)
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
    def _complete_color_cycle(hero_cards, cards_to_play, step, turn):
        if len(cards_to_play) < 4:
            next_color = COLOR_CYCLE[(COLOR_CYCLE.index(cards_to_play[-1].color) + 1) % 3]

            for _, cards in hero_cards.items():
                cond = None
                for card in cards:
                    if turn % 2 == 1:
                        cond = (card.color == next_color)
                    else:
                        cond = (card.color != next_color)
                    if (cond and card not in cards_to_play) or (card.type == CardType.COUNTER and TurnPlayer._have_more_than_one_counter(hero_cards)):
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
                try:
                    cards_left.remove(index)
                except ValueError:
                    pass
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

    @staticmethod
    def _have_more_than_one_counter(hero_cards):
        counter = 0

        for _, cards in hero_cards.items():
            for card in cards:
                if card.type == CardType.COUNTER:
                    counter += 1
                    break

        return counter > 1

    @staticmethod
    def _prepare_finish(hero_cards, last_color, turn):
        cards_to_play = []

        blue_cards_other_than_counter, red_cards_other_than_counter, green_cards_other_than_counter = [], [], []
        if hero_cards.get("Thor", []):
            blue_cards_other_than_counter = [x for x in hero_cards["Thor"]]
        if hero_cards.get("Albedo", []):
            if TurnPlayer._have_more_than_one_counter(hero_cards):
                blue_cards_other_than_counter = [x for x in hero_cards["Albedo"]]
            else:
                blue_cards_other_than_counter += [x for x in hero_cards["Albedo"] if x.type in ["attack", "malus", "ultimate"]]
        if hero_cards.get("Freyr", []):
            red_cards_other_than_counter = [x for x in hero_cards["Freyr"]]
        if hero_cards.get("Jörmungand", []):
            green_cards_other_than_counter = [x for x in hero_cards["Jörmungand"]]

        len_bcotc = len(blue_cards_other_than_counter)
        len_rcotc = len(red_cards_other_than_counter)
        len_gcotc = len(green_cards_other_than_counter)

        for _, cards in hero_cards.items():
            for card in cards:
                if card.color == "blue":
                    if TurnPlayer._have_more_than_one_counter(hero_cards):
                        if len_bcotc >= 2 and card not in cards_to_play:
                            cards_to_play.append(card)
                            len_bcotc -= 1
                            continue
                    else:
                        if card.type in ["attack", "malus", "ultimate"] and len_bcotc >= 2 and card not in cards_to_play:
                            cards_to_play.append(card)
                            len_bcotc -= 1
                            continue
                if card.color == "red":
                    if len_rcotc >= 2 and card not in cards_to_play:
                        cards_to_play.append(card)
                        len_rcotc -= 1
                        continue
                if card.color == "green":
                    if len_gcotc >= 2 and card not in cards_to_play:
                        cards_to_play.append(card)
                        len_gcotc -= 1
                        continue
            if len(cards_to_play) >= 4:
                break

        return cards_to_play

    @staticmethod
    def _finish_him(hero_cards, last_color, turn):
        cards_to_play = []

        for _, cards in hero_cards.items():
            for card in cards:
                if card.type in ["attack", "malus", "ultimate"] and card.color == "blue":
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 1:
                break

        for _, cards in hero_cards.items():
            for card in cards:
                if card.color == "red" and card not in cards_to_play:
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 2:
                break

        for _, cards in hero_cards.items():
            for card in cards:
                if card.color == "green" and card not in cards_to_play:
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 3:
                break

        for _, cards in hero_cards.items():
            for card in cards:
                if card.type == CardType.COUNTER and card not in cards_to_play:
                    cards_to_play.append(card)
                    break
            if len(cards_to_play) == 4:
                break

        return cards_to_play

class FloorThree(Floor):
    def __init__(self):
        super().__init__()

    def enter_level(self):
        super().enter_level((970, 550), 2)

    def restart_floor(self):
        super().restart_floor()

    def check_step(self):
        return super().check_step()

    def filter_cards_by_hero(self, cards):
        return super().filter_cards_by_hero(cards)

    def get_cards_to_play(self, hero_cards, last_color, step, turn):
        return TurnPlayer.get_cards_to_play(hero_cards, last_color, step, turn)

    def play_turn(self, cards):
        super().play_turn(cards)

    def play(self, step, cards, last_color, turn):
        return super().play(step, cards, last_color, turn)

    def run(self):
        while True:
            try:
                super().run()
                break
            except Exception as e:
                if "Cooldown exceeded." in str(e):
                    print("Cooldown exceeded, restarting floor 3")
                    self.restart_floor()
                    continue
                elif "Finish him failed, restarting floor 3" in str(e):
                    print("Finish him failed, restarting floor 3")
                    self.restart_floor()
                    continue
                else:
                    print(f"An error occurred: {e}")
                    exit(1)
