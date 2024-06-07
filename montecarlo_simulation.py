from blackjack import Blackjack


def get_hand_from_input() -> list:
    while True:
        try:
            player_hand_input = input("Enter player hand as comma-separated values (e.g., 10,6): ")
            player_hand = [int(card) for card in player_hand_input.split(',')]
            if (len(player_hand) == 2 and all(card in range(2, 12) for card in player_hand)
                    and player_hand[0] + player_hand[1] < 21):
                return player_hand
            else:
                print("Invalid input. Please enter two card values (2-11) that sums up to less than 21.")
        except ValueError:
            print("Invalid input. Please enter two integer values separated by a comma.")


def get_dealer_card_from_input() -> int:
    while True:
        try:
            dealer_card_input = int(input("Enter dealer's upcard (2-11): "))
            if 2 <= dealer_card_input <= 11:
                return dealer_card_input
            else:
                print("Invalid input. Please enter a card value between 1 and 11.")
        except ValueError:
            print("Invalid input. Please enter an integer value between 1 and 11.")


def main():
    game = Blackjack()
    player_hand = get_hand_from_input()
    dealer_card = get_dealer_card_from_input()

    results = game.simulate_all_actions(player_hand, dealer_card)
    actions = {'h': 'hit', 's': 'stand'}

    for action, prob in results.items():
        print(f"Probability of winning if you {actions[action]}: {prob:.2%}")
    print("Keep in mind, the optimal action may be to double or split!")


if __name__ == "__main__":
    main()
