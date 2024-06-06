import random


class Blackjack:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.player_hand = []
        self.dealer_hand = 0

    def deal_hard(self):
        while True:
            self.player_hand = [random.choice(self.deck), random.choice(self.deck)]
            player_sum = self.player_hand[0] + self.player_hand[1]
            if self.player_hand[0] != 11 and self.player_hand[1] != 11 and 7 < player_sum < 18:
                break
        self.dealer_hand = random.choice(self.deck)

    def deal_soft(self):
        while True:
            self.player_hand = [random.choice(self.deck), random.choice(self.deck)]
            if (
                    (self.player_hand[0] == 11) != (self.player_hand[1] == 11)
                    and self.player_hand[0] + self.player_hand[1] != 21
            ):
                break
        self.dealer_hand = random.choice(self.deck)

    def deal_pairs(self):
        self.player_hand = [random.choice(self.deck)]
        self.player_hand.append(self.player_hand[0])
        self.dealer_hand = random.choice(self.deck)

    def deal_all(self):
        while True:
            self.player_hand = [random.choice(self.deck), random.choice(self.deck)]
            player_sum = self.player_hand[0] + self.player_hand[1]
            if player_sum != 21:
                if (
                    self.player_hand[0] == self.player_hand[1] or
                    self.player_hand[0] == 11 or self.player_hand[1] == 11 or
                    7 < player_sum < 18
                ):
                    break
        self.dealer_hand = random.choice(self.deck)

    @staticmethod
    def hand_value(hand):
        hand_copy = hand.copy()  # Create a copy of the hand
        value = sum(hand_copy)
        while value > 21 and 11 in hand_copy:
            hand_copy[hand_copy.index(11)] = 1
            value = sum(hand_copy)
        return value

    @staticmethod
    def is_soft_hand(hand):
        return 11 in hand and sum(hand) <= 21

    @staticmethod
    def is_pairs(hand):
        return hand[0] == hand[1]

    def basic_strategy(self, player_hand, dealer_upcard):
        hard_hands = {
            20: ['s'] * 10,
            19: ['s'] * 10,
            18: ['s'] * 10,
            17: ['s'] * 10,
            16: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
            15: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
            14: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
            13: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
            12: ['h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
            11: ['d'] * 10,
            10: ['d'] * 8 + ['h', 'h'],
            9: ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],
            8: ['h'] * 10
        }
        soft_hands = {
            (11, 9): ['s'] * 10,
            (11, 8): ['s'] * 4 + ['d'] + ['s'] * 5,
            (11, 7): ['d'] * 5 + ['s'] * 2 + ['h'] * 3,
            (11, 6): ['h'] + ['d'] * 4 + ['h'] * 5,
            (11, 5): ['h'] * 2 + ['d'] * 3 + ['h'] * 5,
            (11, 4): ['h'] * 2 + ['d'] * 3 + ['h'] * 5,
            (11, 3): ['h'] * 3 + ['d'] * 2 + ['h'] * 5,
            (11, 2): ['h'] * 3 + ['d'] * 2 + ['h'] * 5
        }
        pairs = {
            (11, 11): ['y'] * 10,
            (10, 10): ['s'] * 10,
            (9, 9): ['y'] * 5 + ['s'] + ['y'] * 2 + ['s'] * 2,
            (8, 8): ['y'] * 10,
            (7, 7): ['y'] * 6 + ['h'] * 4,
            (6, 6): ['y'] * 5 + ['h'] * 5,
            (5, 5): ['d'] * 8 + ['h'] * 2,
            (4, 4): ['h'] * 3 + ['y'] * 2 + ['h'] * 5,
            (3, 3): ['y'] * 6 + ['h'] * 4,
            (2, 2): ['y'] * 6 + ['h'] * 4
        }

        player_value = self.hand_value(player_hand)
        dealer_index = dealer_upcard - 2

        if self.is_pairs(player_hand):
            print(f"Checking pairs hand strategy matrix for player value: {player_value} (pairs)")
            pair_value = (player_hand[0], player_hand[1])
            if pair_value in pairs:
                print(
                    f"Pairs hand {player_hand} against dealer {dealer_upcard}: "
                    f"{pairs[pair_value][dealer_index]}"
                )
                return pairs[pair_value][dealer_index]
        elif self.is_soft_hand(player_hand):
            print(f"Checking soft hand strategy matrix for player value: {player_value} (soft total)")
            soft_total = player_value - 11
            if (11, soft_total) in soft_hands:
                print(
                    f"Soft hand {player_hand} against dealer {dealer_upcard}: "
                    f"{soft_hands[(11, soft_total)][dealer_index]}"
                )
                return soft_hands[(11, soft_total)][dealer_index]
        else:
            print(f"Checking hard hand strategy matrix for player value: {player_value}")
            if player_value in hard_hands:
                print(
                    f"Hard hand {player_hand} against dealer {dealer_upcard}: "
                    f"{hard_hands[player_value][dealer_index]}"
                )
                return hard_hands[player_value][dealer_index]

        print("No specific strategy found, defaulting to 'ERROR'")
        return 'ERROR'

    def get_feedback(self, action):
        correct_action = self.basic_strategy(self.player_hand, self.dealer_hand)
        if action == correct_action:
            return "Correct action!", 1
        else:
            action = {
                'h': 'hit',
                's': 'stand',
                'd': 'double',
                'y': 'split'
            }.get(correct_action, 'Unknown action')

            return f"Wrong action. The correct action was {action}.", 0

    def play(self, deal_type='all'):
        while True:
            if deal_type == 'hard':
                self.deal_hard()
            elif deal_type == 'soft':
                self.deal_soft()
            elif deal_type == 'pairs':
                self.deal_pairs()
            elif deal_type == 'all':
                self.deal_all()

            print(f"Player's hand: {self.player_hand}")
            print(f"Dealer's upcard: {self.dealer_hand}")

            while True:
                action = input("Enter action (h: hit, s: stand, d: double, y: split, e: end): ").strip().lower()
                if action == 'e':
                    print("Ending game.")
                    return
                elif action in ['h', 's', 'd', 'y']:
                    feedback = self.get_feedback(action)
                    print(feedback)
                    break
                else:
                    print("Invalid action. Please enter h, s, d, or e.")
            print("\nStarting a new game...\n")


if __name__ == "__main__":
    game = Blackjack()
    while True:
        user_input = input("Choose which hands are dealt: [H]ard, [S]oft [P]airs or [A]ll: ")
        if user_input.lower() in ['h', 's', 'p', 'a']:
            mode = {
                'h': 'hard',
                's': 'soft',
                'p': 'pairs',
                'a': 'all'
            }.get(user_input.lower())
            print(f"Starting game. Dealing {mode}")
            game.play(mode)
            break
        else:
            pass
