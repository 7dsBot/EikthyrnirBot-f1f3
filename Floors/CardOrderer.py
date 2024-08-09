class CardOrderer:
    def __init__(self, cards_to_play, cards):
        self.cards_to_play = cards_to_play
        self.cards = cards
        self.ordered_cards = self.cards_to_play.copy()

    def order_card_indexes(self):
        for i in range(len(self.cards_to_play)):
            card = self.ordered_cards[i]

            if card == 69:
                continue

            actual_card = self._find_card_by_index(card)

            adjacent_cards = self._get_adjacent_cards(actual_card)
            offset = self._calculate_offset(adjacent_cards)

            self._adjust_future_indexes(card, i, offset)

            self._update_cards_copy(actual_card)

        return self.ordered_cards

    def _find_card_by_index(self, index):
        return next((x for x in self.cards if x.index == index), None)

    def _get_adjacent_cards(self, actual_card):
        indexes = [actual_card.index - 2, actual_card.index - 1, actual_card.index + 1, actual_card.index + 2]

        before_prev_card = self._find_card_by_index(indexes[0]) if indexes[0] > 0 else None
        prev_card = self._find_card_by_index(indexes[1]) if indexes[1] > 0 else None
        next_card = self._find_card_by_index(indexes[2]) if indexes[2] < 9 else None
        after_next_card = self._find_card_by_index(indexes[3]) if indexes[3] < 9 else None

        return before_prev_card, prev_card, next_card, after_next_card

    def _calculate_offset(self, adjacent_cards):
        before_prev_card, prev_card, next_card, after_next_card = adjacent_cards
        offset = 0

        if prev_card and next_card and self._are_cards_matching(prev_card, next_card):
            offset += 1
            if before_prev_card and self._are_cards_matching(before_prev_card, next_card):
                offset += 1
            elif after_next_card and self._are_cards_matching(next_card, after_next_card):
                offset += 1

        return offset

    def _are_cards_matching(self, card1, card2):
        return card1 != None and card2 != None and card1.level != 3 and card1.hero == card2.hero and card1.name == card2.name and card1.level == card2.level

    def _adjust_future_indexes(self, card, current_index, offset):
        for i in range(current_index + 1, len(self.cards_to_play)):
            if self.ordered_cards[i] <= card:
                self.ordered_cards[i] += (1 + offset)

    def _update_cards_copy(self, actual_card):
        self.cards.remove(actual_card)
        for i in range(len(self.cards)):
            self.cards[i].index = i + 1 + (8 - len(self.cards))
