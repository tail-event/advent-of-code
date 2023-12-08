import os
import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Self

NUMERIC_VALS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    **{str(i): i for i in range(2, 10)},
}


@dataclass(frozen=True, slots=True)
class Card:
    symbol: str

    @property
    def value(self) -> int:
        return NUMERIC_VALS[self.symbol]

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.value == other.value

    def is_joker(self) -> bool:
        return self.symbol == "J"


class HandKind(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int

    def __str__(self) -> str:
        return f"Hand({''.join(c.symbol for c in self.cards)})"

    def has_jokers(self) -> bool:
        return any(card.is_joker() for card in self.cards)

    @property
    def kind_using_jokers(self) -> HandKind:
        best_kind = self.kind
        if best_kind == HandKind.FIVE_OF_A_KIND:
            return best_kind

        jokers_indices = [i for i in range(len(self.cards)) if self.cards[i] == Card("J")]
        most_common_card, most_common_count = [x for x in self.counts_most_common if x[0] != Card("J")][0]

        new_cards = list(self.cards)
        for joker_idx in jokers_indices:
            new_cards[joker_idx] = most_common_card
        new_hand = Hand(cards=new_cards, bid=self.bid)

        new_hand_counts_most_common = new_hand.counts_most_common
        most_common_card, most_common_count = new_hand_counts_most_common[0]
        if most_common_count == 5:
            best_kind = HandKind.FIVE_OF_A_KIND

        elif most_common_count == 4:
            best_kind = HandKind.FOUR_OF_A_KIND

        elif most_common_count == 3:
            second_most_common_card, second_most_common_count = new_hand_counts_most_common[1]
            if second_most_common_count == 2:
                best_kind = HandKind.FULL_HOUSE
            else:
                best_kind = HandKind.THREE_OF_A_KIND

        elif most_common_count == 2:
            second_most_common_card, second_most_common_count = new_hand_counts_most_common[1]
            if second_most_common_count == 2:
                best_kind = HandKind.TWO_PAIR
            else:
                best_kind = HandKind.ONE_PAIR

        return best_kind

    def get_best_kind(self, use_jokers: bool) -> HandKind:
        if use_jokers and self.has_jokers():
            return self.kind_using_jokers
        return self.kind

    @property
    def kind(self) -> HandKind:
        counts_most_common = self.counts_most_common
        most_common = counts_most_common[0][1]
        if most_common == 5:
            return HandKind.FIVE_OF_A_KIND
        elif most_common == 4:
            return HandKind.FOUR_OF_A_KIND
        elif most_common == 3:
            if counts_most_common[1][1] == 2:
                return HandKind.FULL_HOUSE
            return HandKind.THREE_OF_A_KIND
        elif most_common == 2:
            if counts_most_common[1][1] == 2:
                return HandKind.TWO_PAIR
            return HandKind.ONE_PAIR
        return HandKind.HIGH_CARD

    def __lt__(self, other: Self) -> bool:
        for card, other_card in zip(self.cards, other.cards):
            if card == other_card:
                continue
            return True if card < other_card else False
        raise RuntimeError()

    def __eq__(self, other: object) -> bool:
        if not isinstance(object, Hand):
            return False
        return self.counts == other.counts

    @cached_property
    def counts_most_common(self) -> list[tuple[Card, int]]:
        return self.counts.most_common()

    @cached_property
    def counts(self) -> Counter:
        return Counter(self.cards)


def first_part_solution(hands: list[Hand], use_jokers: bool = False) -> int:
    groups: dict[HandKind, list[Hand]] = {}
    for hand in hands:
        hand_kind = hand.get_best_kind(use_jokers=use_jokers)
        groups.setdefault(hand_kind, []).append(hand)

    for group in groups.keys():
        groups[group].sort()

    res = 0
    rank = 1
    for kind in reversed(HandKind):
        if kind not in groups:
            continue

        for hand in groups[kind]:
            res += hand.bid * rank
            rank += 1

    return res


def second_part_solution(hands: list[Hand]) -> int:
    NUMERIC_VALS["J"] = 1
    return first_part_solution(hands, use_jokers=True)


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        t0 = time.perf_counter()
        hands = []
        for line in f:
            hand, bid = line.split()
            hands.append(Hand(cards=[Card(symbol) for symbol in hand], bid=int(bid)))

        first_part_res = first_part_solution(hands)
        print(f"First part solution: {first_part_res}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        second_part_res = second_part_solution(hands)
        print(f"Second part solution: {second_part_res}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
