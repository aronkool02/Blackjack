import tkinter as tk
from PIL import Image, ImageTk
from blackjack import Blackjack
import random


class BlackjackGUI:
    def __init__(self, inner_root):
        self.game_type_window = None
        self.game = Blackjack()
        self.root = inner_root
        self.root.title("Blackjack Game")
        self.responses = []
        self.wrong_hands = []
        self.game_type = "deal"

        self.card_images = {}  # Dictionary to store loaded card images

        self.info_label = tk.Label(inner_root, text="Welcome to Blackjack!", font=("Helvetica", 18))
        self.info_label.pack()

        self.player_hand_label = tk.Label(inner_root, text="", font=("Helvetica", 16))
        self.player_hand_label.pack()

        self.dealer_hand_label = tk.Label(inner_root, text="", font=("Helvetica", 16))
        self.dealer_hand_label.pack()

        self.feedback_frame = tk.Frame(inner_root)
        self.feedback_frame.pack()

        self.stand_button = tk.Button(inner_root, text="[S] Stand", command=self.stand, font=("Helvetica", 14))
        self.stand_button.pack(side=tk.LEFT)

        self.double_button = tk.Button(inner_root, text="[D] Double", command=self.double, font=("Helvetica", 14))
        self.double_button.pack(side=tk.LEFT)

        self.hit_button = tk.Button(inner_root, text="[K] Hit", command=self.hit, font=("Helvetica", 14))
        self.hit_button.pack(side=tk.LEFT)

        self.double_button = tk.Button(inner_root, text="[L] Split", command=self.split, font=("Helvetica", 14))
        self.double_button.pack(side=tk.LEFT)

        self.end_button = tk.Button(inner_root, text="[E] End", command=self.end_game, font=("Helvetica", 14))
        self.end_button.pack(side=tk.RIGHT)

        self.root.bind('k', lambda event: self.hit())
        self.root.bind('s', lambda event: self.stand())
        self.root.bind('d', lambda event: self.double())
        self.root.bind('l', lambda event: self.split())
        self.root.bind('e', lambda event: self.end_game())

        self.load_card_images()
        self.ask_game_type()

    def load_card_images(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for value in values:
                card_name = f"{value}_of_{suit}"
                try:
                    image = Image.open(f"cards/{card_name}.png")
                    scaled_image = image.resize((int(image.width * 0.3), int(image.height * 0.3)),
                                                Image.Resampling.LANCZOS)
                    self.card_images[card_name] = ImageTk.PhotoImage(scaled_image)
                except Exception as e:
                    print(f"Error loading image for {card_name}: {e}")

    def ask_game_type(self):
        self.game_type_window = tk.Toplevel(self.root)
        self.game_type_window.title("Select Game Type")

        tk.Label(self.game_type_window, text="Select the type of game:", font=("Helvetica", 16)).pack()

        tk.Button(self.game_type_window, text="Deal All",
                  command=lambda: self.set_game_type("deal_all"), font=("Helvetica", 14)).pack()
        tk.Button(self.game_type_window, text="Deal Soft",
                  command=lambda: self.set_game_type("deal_soft"), font=("Helvetica", 14)).pack()
        tk.Button(self.game_type_window, text="Deal Hard",
                  command=lambda: self.set_game_type("deal_hard"), font=("Helvetica", 14)).pack()
        tk.Button(self.game_type_window, text="Deal Pairs",
                  command=lambda: self.set_game_type("deal_pairs"), font=("Helvetica", 14)).pack()

    def set_game_type(self, game_type):
        self.game_type = game_type
        self.game_type_window.destroy()
        self.new_game()

    def new_game(self):
        getattr(self.game, self.game_type)()
        self.update_display()

    def update_display(self):
        self.player_hand_label.config(text=f"Player's hand: {self.game.player_hand}")
        self.dealer_hand_label.config(text=f"Dealer's upcard: {self.game.dealer_hand}")

        # Display card images (example for player's hand)
        for widget in self.player_hand_label.winfo_children():
            widget.destroy()

        for card in self.game.player_hand:
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            suit = random.choice(suits)
            if card == 10:
                tens = ['10', 'jack', 'queen', 'king']
                card = random.choice(tens)
            elif card == 11:
                card = 'ace'
            card_name = f"{card}_of_{suit}"
            card_image = self.card_images.get(card_name)
            print(f"Looking up card image for: {card_name}")  # Debugging print statement
            if card_image:
                card_label = tk.Label(self.player_hand_label, image=card_image)
                card_label.pack(side=tk.LEFT)
            else:
                print(f"Error: No image found for {card_name}")

    def hit(self):
        self.perform_action('h')

    def stand(self):
        self.perform_action('s')

    def double(self):
        self.perform_action('d')

    def split(self):
        self.perform_action('y')

    def perform_action(self, action):
        feedback, result = self.game.get_feedback(action)
        self.responses.append(result)
        if result == 0:
            self.wrong_hands.append((self.game.player_hand.copy(), self.game.dealer_hand))

        color = "green" if result == 1 else "red"
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        feedback_label = tk.Label(self.feedback_frame, text=feedback, font=("Helvetica", 16), fg=color)
        feedback_label.pack()

        self.new_game()

    def end_game(self):
        correct_count = sum(self.responses)
        total_count = len(self.responses)
        percentage_correct = (correct_count / total_count) * 100 if total_count > 0 else 0

        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")

        tk.Label(stats_window, text=f"Correct answers: {correct_count} / {total_count}", font=("Helvetica", 16)).pack()
        tk.Label(stats_window, text=f"Percentage correct: {percentage_correct:.2f}%", font=("Helvetica", 16)).pack()

        tk.Label(stats_window, text="Wrong hands:", font=("Helvetica", 16)).pack()
        wrong_hands_text = "\n".join([f"Player: {ph}, Dealer: {dh}" for ph, dh in self.wrong_hands])
        tk.Label(stats_window, text=wrong_hands_text, font=("Helvetica", 12)).pack()

        tk.Button(stats_window, text="Done", command=self.quit_program, font=("Helvetica", 14)).pack()

    def quit_program(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    gui = BlackjackGUI(root)
    root.mainloop()
