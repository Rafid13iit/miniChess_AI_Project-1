import tkinter as tk
from tkinter import messagebox
from .game_setup import GameSetupDialog
from .board_view import BoardView
from ..game import MinichessGame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.game = None
        self.selected_piece = None
        self.start_screen()

    def start_screen(self):
        self.root.geometry("400x300")
        
        title = tk.Label(self.root, text="MiniChess", font=('Arial', 24, 'bold'))
        title.pack(pady=20)
        
        new_game_btn = tk.Button(self.root, text="New Game", command=self.setup_game)
        new_game_btn.pack(pady=10)
        
        quit_btn = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit_btn.pack(pady=10)

    def setup_game(self):
        setup_dialog = GameSetupDialog(self.root)
        self.root.wait_window(setup_dialog.window)
        self.game = setup_dialog.start_game()
        
        if self.game:
            self.start_game_ui()

    def start_game_ui(self):
        self.root.geometry("400x500")
        
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create frame for game info
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Status label shows current player and selected piece
        self.status_label = tk.Label(info_frame, 
                                   text=f"{self.game.current_player.capitalize()}'s turn", 
                                   font=('Arial', 12))
        self.status_label.pack(pady=5)
        
        # Create board view
        self.board_view = BoardView(self.root, self.game.board, self.on_cell_clicked)
        
        # If first player is AI, play their turn
        if self.game.players[self.game.current_player]:
            self.root.after(500, self.play_ai_turn)

    def on_cell_clicked(self, col, row):
        # Ignore clicks during AI turn
        if self.game.players[self.game.current_player]:
            return
            
        piece = self.game.board.board[row][col]
        
        # If no piece is selected
        if not self.selected_piece:
            if piece and piece.color == self.game.current_player:
                self.selected_piece = (col, row)
                self.board_view.highlight_selected(col, row)
                self.status_label.config(text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}")
        
        # If a piece is already selected
        else:
            start_col, start_row = self.selected_piece
            
            # If clicking the same piece, deselect it
            if (col, row) == (start_col, start_row):
                self.selected_piece = None
                self.board_view.update(self.game.board)
                self.status_label.config(text=f"{self.game.current_player.capitalize()}'s turn")
                return
            
            # Try to move the selected piece
            if self.game.board.move_piece(self.selected_piece, (col, row)):
                # Move was successful
                self.board_view.update(self.game.board)
                self.selected_piece = None
                
                # Switch players
                self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
                self.status_label.config(text=f"{self.game.current_player.capitalize()}'s turn")
                
                # Check for checkmate
                if self.game.board.is_checkmate(self.game.current_player):
                    winner = 'Black' if self.game.current_player == 'white' else 'White'
                    messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
                    self.start_screen()
                    return
                
                # If next player is AI, play their turn
                if self.game.players[self.game.current_player]:
                    self.root.after(500, self.play_ai_turn)
            else:
                # Invalid move, just update the selection
                if piece and piece.color == self.game.current_player:
                    self.selected_piece = (col, row)
                    self.board_view.highlight_selected(col, row)
                    self.status_label.config(text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}")
                else:
                    self.selected_piece = None
                    self.board_view.update(self.game.board)
                    self.status_label.config(text=f"Invalid move. {self.game.current_player.capitalize()}'s turn")

    def play_ai_turn(self):
        ai_player = self.game.players[self.game.current_player]
        start_pos, end_pos = ai_player.get_best_move(self.game.board)
        
        # Highlight AI's move
        self.board_view.highlight_selected(*start_pos)
        self.status_label.config(text=f"AI moving {chr(start_pos[0]+97)}{start_pos[1]+1} to {chr(end_pos[0]+97)}{end_pos[1]+1}")
        self.root.update()
        
        # Wait a bit to show the selection
        self.root.after(500)
        
        # Make the move
        self.game.board.move_piece(start_pos, end_pos)
        self.board_view.update(self.game.board)
        
        # Switch players
        self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
        self.status_label.config(text=f"{self.game.current_player.capitalize()}'s turn")
        
        # Check for checkmate
        if self.game.board.is_checkmate(self.game.current_player):
            winner = 'Black' if self.game.current_player == 'white' else 'White'
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            self.start_screen()