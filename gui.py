import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from blackjack import Blackjack
import random
from resource_path import resource_path


class BlackjackGUI:
    def __init__(self, inner_root) -> None:
        self.game_type_window = None
        self.game = Blackjack()
        self.root = inner_root
        self.root.withdraw()
        self.root.title("Blackjack Game")
        self.responses = []
        self.wrong_hands = []
        self.game_type = "deal"
        self.stats_root = None
        self.restart = 0
        self.font = "Helvetica"
        self.button_font_size = 14

        self.card_images = {}  # Dictionary to store loaded card images

        self.info_label = tk.Label(inner_root, text="Welcome to Blackjack!", font=(self.font, 24))
        self.info_label.pack(pady=10, padx=10)

        self.dealer_hand_label = tk.Label(inner_root, text="", font=(self.font, 20))
        self.dealer_hand_label.pack(pady=10, padx=10)

        self.player_hand_label = tk.Label(inner_root, text="", font=(self.font, 20))
        self.player_hand_label.pack(pady=10, padx=10)

        self.feedback_frame = tk.Frame(inner_root)
        self.feedback_frame.pack(pady=10, padx=10)

        self.stand_button = tk.Button(inner_root, text="[S] Stand", command=self.stand, font=(
            self.font, self.button_font_size
        ))
        self.stand_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.double_button = tk.Button(inner_root, text="[D] Double", command=self.double, font=(
            self.font, self.button_font_size
        ))
        self.double_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.hit_button = tk.Button(inner_root, text="[K] Hit", command=self.hit, font=(
            self.font, self.button_font_size
        ))
        self.hit_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.split_button = tk.Button(inner_root, text="[L] Split", command=self.split, font=(
            self.font, self.button_font_size
        ))
        self.split_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.end_button = tk.Button(inner_root, text="[E] End", command=self.end_game, font=(
            self.font, self.button_font_size
        ))
        self.end_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.root.bind('k', lambda event: self.hit())
        self.root.bind('s', lambda event: self.stand())
        self.root.bind('d', lambda event: self.double())
        self.root.bind('l', lambda event: self.split())
        self.root.bind('e', lambda event: self.end_game())

        self.load_card_images()
        self.ask_game_type()

    def update_fonts(self):
        for widget in [self.info_label, self.dealer_hand_label, self.player_hand_label, self.stand_button,
                       self.double_button, self.hit_button, self.split_button, self.end_button]:
            current_font = tkfont.Font(font=widget.cget("font"))
            font_size = current_font.cget("size")
            widget.config(font=(self.font, font_size))

        if self.game_type_window:
            for widget in self.game_type_window.winfo_children():
                current_font = tkfont.Font(font=widget.cget("font"))
                font_size = current_font.cget("size")
                widget.config(font=(self.font, font_size))

    def load_card_images(self) -> None:
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        absolute_path = resource_path("cards")
        for suit in suits:
            for value in values:
                card_name = f"{value}_of_{suit}"
                try:
                    image = Image.open(f"{absolute_path}/{card_name}.png")
                    scaled_image = image.resize((int(image.width * 0.3), int(image.height * 0.3)),
                                                Image.Resampling.LANCZOS)
                    self.card_images[card_name] = ImageTk.PhotoImage(scaled_image)
                except Exception as e:
                    print(f"Error loading image for {card_name}: {e}")

    def ask_game_type(self) -> None:
        self.game_type_window = tk.Toplevel(self.root)
        self.game_type_window.title("Select Game Type")

        # Force focus on the window
        self.game_type_window.lift()
        self.game_type_window.focus_force()

        tk.Label(self.game_type_window, text="Select the type of game:", font=(self.font, 20)).pack(pady=10, padx=10)

        tk.Button(self.game_type_window, text="Deal [A] All",
                  command=lambda: self.set_game_type("deal_all"), font=(
                    self.font, self.button_font_size
                    )).pack(pady=10, padx=10)
        tk.Button(self.game_type_window, text="Deal [S] Soft",
                  command=lambda: self.set_game_type("deal_soft"), font=(
                    self.font, self.button_font_size
                    )).pack(pady=10, padx=10)
        tk.Button(self.game_type_window, text="Deal [H] Hard",
                  command=lambda: self.set_game_type("deal_hard"), font=(
                    self.font, self.button_font_size
                    )).pack(pady=10, padx=10)
        tk.Button(self.game_type_window, text="Deal [P] Pairs",
                  command=lambda: self.set_game_type("deal_pairs"), font=(
                    self.font, self.button_font_size
                    )).pack(pady=10, padx=10)

        self.game_type_window.bind('a', lambda event: self.set_game_type("deal_all"))
        self.game_type_window.bind('s', lambda event: self.set_game_type("deal_soft"))
        self.game_type_window.bind('h', lambda event: self.set_game_type("deal_hard"))
        self.game_type_window.bind('p', lambda event: self.set_game_type("deal_pairs"))
        self.game_type_window.bind('c', lambda event: (setattr(self, "font", "Comic Sans MS"), self.update_fonts()))

    def set_game_type(self, game_type) -> None:
        self.game_type = game_type
        self.game_type_window.destroy()
        self.root.deiconify()
        self.new_game()

    def new_game(self) -> None:
        getattr(self.game, self.game_type)()
        self.update_display()

    def update_display(self) -> None:
        # self.player_hand_label.config(text=f"Player's hand: {self.game.player_hand}")
        # self.dealer_hand_label.config(text=f"Dealer's upcard: {self.game.dealer_hand}")

        # Clear previous card images
        for widget in self.player_hand_label.winfo_children():
            widget.destroy()

        for widget in self.dealer_hand_label.winfo_children():
            widget.destroy()

        # Display rtp in Comic Sans MS mode
        if self.font == "Comic Sans MS":
            rtp_value = self.game.get_rtp()
            color = "red" if rtp_value < 0 else "green"
            rtp_label = tk.Label(self.dealer_hand_label, text="RTP", font=(self.font, 20))
            rtp_label.pack(side=tk.TOP)
            rtp_label = tk.Label(self.dealer_hand_label, text=f"{rtp_value * 10:.3f}", font=(self.font, 20), fg=color)
            rtp_label.pack(side=tk.TOP)

        # Display dealer's upcard
        dealer_upcard = self.game.dealer_hand
        dealer_card_name = self.get_card_name(dealer_upcard)
        dealer_card_image = self.card_images.get(dealer_card_name)
        if dealer_card_image:
            dealer_card_label = tk.Label(self.dealer_hand_label, image=dealer_card_image)
            dealer_card_label.image = dealer_card_image  # Keep a reference to the image
            dealer_card_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Display player's hand
        for card in self.game.player_hand:
            card_name = self.get_card_name(card)
            card_image = self.card_images.get(card_name)
            if card_image:
                card_label = tk.Label(self.player_hand_label, image=card_image)
                card_label.image = card_image  # Keep a reference to the image
                card_label.pack(side=tk.LEFT, padx=20)

    @staticmethod
    def get_card_name(card) -> str:
        suit = random.choice(['hearts', 'diamonds', 'clubs', 'spades'])
        if card == 10:
            card = random.choice(['10', 'jack', 'queen', 'king'])
        elif card == 11:
            card = 'ace'
        return f"{card}_of_{suit}"

    def hit(self) -> None:
        self.perform_action('h')

    def stand(self) -> None:
        self.perform_action('s')

    def double(self) -> None:
        self.perform_action('d')

    def split(self) -> None:
        if self.game.player_hand[0] == self.game.player_hand[1]:
            self.perform_action('y')
        else:
            self.perform_action('n')

    def perform_action(self, action) -> None:
        feedback, result = self.game.get_feedback(action)
        if action == 'n':
            print("Split is not a valid action")
            for widget in self.feedback_frame.winfo_children():
                widget.destroy()
            feedback_label = tk.Label(self.feedback_frame, text=f"You noob!", font=(self.font, 20), fg="red")
            feedback_label.pack()
            feedback_label = tk.Label(
                self.feedback_frame,
                text=(f"You can't split {'ace' if self.game.player_hand[0] == 11 else self.game.player_hand[0]} "
                      f"and {'ace' if self.game.player_hand[1] == 11 else self.game.player_hand[1]}"),
                font=(self.font, 20),
                fg="red"
            )
            feedback_label.pack()
        else:
            self.responses.append(result)
            if result == 0:
                self.wrong_hands.append((self.game.player_hand.copy(), self.game.dealer_hand))

            color = "green" if result == 1 else "red"
            for widget in self.feedback_frame.winfo_children():
                widget.destroy()
            action_dict = {
                'h': 'hit',
                's': 'stood',
                'd': 'doubled',
                'y': 'split'
            }.get(action, 'Unknown action')
            feedback_label = tk.Label(self.feedback_frame, text=f"You {action_dict}!", font=(self.font, 20), fg=color)
            feedback_label.pack()
            feedback_label = tk.Label(self.feedback_frame, text=feedback, font=(self.font, 20), fg=color)
            feedback_label.pack()

            self.new_game()

    def end_game(self) -> None:
        # Create a new root window for the stats window
        self.stats_root = tk.Tk()
        self.stats_root.title("Game Statistics")

        correct_count = sum(self.responses)
        total_count = len(self.responses)
        percentage_correct = (correct_count / total_count) * 100 if total_count > 0 else 0

        (tk.Label(self.stats_root, text=f"Correct answers: {correct_count} / {total_count}", font=(self.font, 20))
         .pack(pady=10, padx=10))
        (tk.Label(self.stats_root, text=f"Percentage correct: {percentage_correct:.2f}%", font=(self.font, 20))
         .pack(padx=10))

        if self.wrong_hands:
            tk.Label(self.stats_root, text="Wrong hands:", font=(self.font, 20)).pack(pady=10, padx=10)
            wrong_hands_text = "\n".join([f"Player: {ph}, Dealer: {dh}" for ph, dh in self.wrong_hands])
            tk.Label(self.stats_root, text=wrong_hands_text, font=(self.font, 16)).pack(padx=10)

        (tk.Button(self.stats_root, text="[E] End", command=self.quit_program,
                   font=(self.font, self.button_font_size))
         .pack(pady=10, padx=10))
        (tk.Button(self.stats_root, text="[R] Restart game", command=self.restart_program,
                   font=(self.font, self.button_font_size))
         .pack(pady=10, padx=10))

        # Force focus on the stats window
        self.stats_root.lift()
        self.stats_root.focus_force()

        # Destroy the main game window
        self.root.destroy()
        self.stats_root.bind('e', lambda event: self.quit_program())
        self.stats_root.bind('r', lambda event: self.restart_program())

    def quit_program(self) -> None:
        self.stats_root.destroy()
        self.root.quit()

    def restart_program(self) -> None:
        self.restart = 1
        self.quit_program()


if __name__ == "__main__":
    while True:
        root = tk.Tk()
        gui = BlackjackGUI(root)
        root.mainloop()

        if gui.restart == 0:
            break
        else:
            gui.restart = 0
