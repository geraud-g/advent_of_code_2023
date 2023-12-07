from dataclasses import dataclass
from itertools import groupby


@dataclass
class Hand:
    hand_type: int
    hand: list[int]
    bid: int


def part_one(input_file: str) -> int:
    hands = get_hands(input_file)
    return get_hands_total_winnings(hands)


def part_two(input_file: str) -> int:
    hands = get_hands(input_file, joker_variant=True)
    return get_hands_total_winnings(hands)


def get_hands_total_winnings(hands: list[Hand]) -> int:
    sorted_hands = sorted(hands, key=lambda h: (h.hand_type, h.hand))
    total = 0
    for idx, hand in enumerate(sorted_hands):
        total += (idx + 1) * hand.bid
    return total


def get_hands(input_file: str, joker_variant: bool = False) -> list[Hand]:
    card_values = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    if joker_variant:
        card_values["J"] = -1

    hands = []
    with open(input_file) as f:
        for line in f.readlines():
            hand, bid = line.strip().split()
            hand = [card_values.get(card) or int(card) for card in hand]
            if joker_variant:
                hand_type = get_hand_type_with_joker_variant(hand)
            else:
                hand_type = get_hand_type(hand)
            hands.append(Hand(hand_type, hand, int(bid)))
    return hands


def get_hand_type(hand: list[int]) -> int:
    sorted_cards = sorted(hand)
    groups = [len(list(g)) for (_, g) in groupby(sorted_cards)]
    sorted_groups = sorted(groups, reverse=True)
    # We add an empty group here only to avoid an IndexError,
    # in case we are evaluating a hand with too many removed jokers
    sorted_groups += [0]
    if sorted_groups[0] == 5:  # Five of a kind
        return 6
    elif sorted_groups[0] == 4:  # Four of a king
        return 5
    elif sorted_groups[0] == 3 and sorted_groups[1] == 2:  # Full house
        return 4
    elif sorted_groups[0] == 3:  # Three of a kind
        return 3
    elif sorted_groups[0] == 2 and sorted_groups[1] == 2:  # Two pairs
        return 2
    elif sorted_groups[0] == 2:  # One pair
        return 1
    else:  # High card
        return 0


def get_hand_type_with_joker_variant(hand: list[int]) -> int:
    hand_upgrades = {0: 1, 1: 3, 2: 4, 3: 5, 4: 5, 5: 6, 6: 6}
    jokers_nbr = sum([1 for card in hand if card == -1])
    cards_without_joker = [card for card in hand if card != -1]
    hand_type = get_hand_type(cards_without_joker)
    for _ in range(jokers_nbr):
        hand_type = hand_upgrades[hand_type]
    return hand_type
