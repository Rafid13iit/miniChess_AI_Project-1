import tkinter as tk
from tkinter import ttk
from ..game import MinichessGame

class GameSetupDialog:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("MiniChess - Game Setup")
        self.window.geometry("300x250")
        self.window.transient(parent)
        self.window.grab_set()

        self.player1_type = tk.StringVar(value='human')
        self.player2_type = tk.StringVar(value='ai')

        self.create_widgets()

    def create_widgets(self):
        # Player 1 (White) setup
        tk.Label(self.window, text="White Player", font=('Arial', 12, 'bold')).pack(pady=(10, 5))
        white_human = tk.Radiobutton(self.window, text="Human", variable=self.player1_type, value='human')
        white_ai = tk.Radiobutton(self.window, text="AI", variable=self.player1_type, value='ai')
        white_human.pack()
        white_ai.pack()

        # Player 2 (Black) setup
        tk.Label(self.window, text="Black Player", font=('Arial', 12, 'bold')).pack(pady=(10, 5))
        black_human = tk.Radiobutton(self.window, text="Human", variable=self.player2_type, value='human')
        black_ai = tk.Radiobutton(self.window, text="AI", variable=self.player2_type, value='ai')
        black_human.pack()
        black_ai.pack()

        # Start Game Button
        start_button = tk.Button(self.window, text="Start Game", command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        game = MinichessGame(self.player1_type.get(), self.player2_type.get())
        self.window.destroy()
        return game