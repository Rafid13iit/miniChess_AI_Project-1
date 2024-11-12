import tkinter as tk
from tkinter import ttk, messagebox
from .game_setup import GameSetupDialog
from .board_view import BoardView
from ..game import MinichessGame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniChess")
        self.game = None
        self.selected_piece = None
        
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        self.center_window(1000, 700)
        
        # Configure styles
        self.setup_styles()
        
        self.start_screen()

    def setup_styles(self):
        """Configure ttk styles for the application"""
        style = ttk.Style()
        style.configure('Title.TLabel', 
                       font=('Helvetica', 36, 'bold'),
                       foreground='#2C3E50',
                       background='#f0f0f0',
                       padding=20)
        
        style.configure('GameButton.TButton',
                       font=('Helvetica', 14),
                       padding=10)
        
        style.configure('Status.TLabel',
                       font=('Helvetica', 12),
                       background='#f0f0f0',
                       padding=5)
        
        style.configure('GameInfo.TFrame',
                       background='#f0f0f0')
        
        style.configure('MainMenu.TFrame',
                       background='#f0f0f0')
        
        style.configure('InGame.TFrame',
                       background='#f0f0f0')

    def center_window(self, width, height):
        """Center the window on the screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def start_screen(self):
        """Create the main menu screen"""
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, style='MainMenu.TFrame')
        main_frame.pack(expand=True, fill='both')
        
        # Logo/Title
        title_frame = ttk.Frame(main_frame, style='MainMenu.TFrame')
        title_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(title_frame,
                 text="♔ MiniChess ♚",
                 style='Title.TLabel').pack(expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame, style='MainMenu.TFrame')
        button_frame.pack(expand=True, pady=20)
        
        # New Game button with hover effect
        new_game_btn = ttk.Button(button_frame,
                                text="New Game",
                                style='GameButton.TButton',
                                command=self.setup_game,
                                width=20)
        new_game_btn.pack(pady=10)
        
        # Quit button
        quit_btn = ttk.Button(button_frame,
                            text="Quit",
                            style='GameButton.TButton',
                            command=self.root.quit,
                            width=20)
        quit_btn.pack(pady=10)

    def setup_game(self):
        """Open game setup dialog"""
        setup_dialog = GameSetupDialog(self.root)
        self.root.wait_window(setup_dialog.window)
        self.game = setup_dialog.start_game()
        
        if self.game:
            self.start_game_ui()

    def start_game_ui(self):
        """Initialize the game interface"""
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main game frame
        game_frame = ttk.Frame(self.root, style='InGame.TFrame')
        game_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Top info frame
        info_frame = ttk.Frame(game_frame, style='GameInfo.TFrame')
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Create menu bar
        menu_frame = ttk.Frame(info_frame)
        menu_frame.pack(fill='x', pady=5)
        
        new_game_btn = ttk.Button(menu_frame,
                                text="New Game",
                                command=self.setup_game,
                                style='GameButton.TButton')
        new_game_btn.pack(side='left', padx=5)
        
        quit_btn = ttk.Button(menu_frame,
                            text="Main Menu",
                            command=self.start_screen,
                            style='GameButton.TButton')
        quit_btn.pack(side='left', padx=5)
        
        # Status label shows current player and selected piece
        self.status_label = ttk.Label(info_frame,
                                    text=f"{self.game.current_player.capitalize()}'s turn",
                                    style='Status.TLabel')
        self.status_label.pack(pady=5)
        
        # Create board view
        board_frame = ttk.Frame(game_frame)
        board_frame.pack(expand=True, pady=10)
        self.board_view = BoardView(board_frame, self.game.board, self.on_cell_clicked)
        
        # If first player is AI, play their turn
        if self.game.players[self.game.current_player]:
            self.root.after(500, self.play_ai_turn)

    def show_game_over(self, winner):
        """Display game over dialog with animations"""
        dialog = tk.Toplevel(self.root)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.configure(bg='#f0f0f0')
        dialog.title("Game Over")
        
        # Center dialog
        dialog_width = 300
        dialog_height = 200
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')
        
        ttk.Label(dialog,
                 text="Game Over!",
                 style='Title.TLabel').pack(pady=10)
        
        ttk.Label(dialog,
                 text=f"{winner} wins!",
                 style='Status.TLabel').pack(pady=10)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(expand=True)
        
        ttk.Button(button_frame,
                  text="New Game",
                  command=lambda: [dialog.destroy(), self.setup_game()],
                  style='GameButton.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame,
                  text="Main Menu",
                  command=lambda: [dialog.destroy(), self.start_screen()],
                  style='GameButton.TButton').pack(side='left', padx=5)

    def on_cell_clicked(self, col, row):
        """Handle cell clicks on the board"""
        # Existing game logic remains unchanged
        if self.game.players[self.game.current_player]:
            return
            
        piece = self.game.board.board[row][col]
        
        if not self.selected_piece:
            if piece and piece.color == self.game.current_player:
                self.selected_piece = (col, row)
                self.board_view.highlight_selected(col, row)
                self.status_label.configure(
                    text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}"
                )
        else:
            start_col, start_row = self.selected_piece
            
            if (col, row) == (start_col, start_row):
                self.selected_piece = None
                self.board_view.update(self.game.board)
                self.status_label.configure(
                    text=f"{self.game.current_player.capitalize()}'s turn"
                )
                return
            
            if self.game.board.move_piece(self.selected_piece, (col, row)):
                self.board_view.update(self.game.board)
                self.selected_piece = None
                
                self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
                self.status_label.configure(
                    text=f"{self.game.current_player.capitalize()}'s turn"
                )
                
                if self.game.board.is_checkmate(self.game.current_player):
                    winner = 'Black' if self.game.current_player == 'white' else 'White'
                    self.show_game_over(winner)
                    return
                
                if self.game.players[self.game.current_player]:
                    self.root.after(500, self.play_ai_turn)
            else:
                if piece and piece.color == self.game.current_player:
                    self.selected_piece = (col, row)
                    self.board_view.highlight_selected(col, row)
                    self.status_label.configure(
                        text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}"
                    )
                else:
                    self.selected_piece = None
                    self.board_view.update(self.game.board)
                    self.status_label.configure(
                        text=f"Invalid move. {self.game.current_player.capitalize()}'s turn"
                    )

    def play_ai_turn(self):
        """Handle AI player moves"""
        ai_player = self.game.players[self.game.current_player]
        start_pos, end_pos = ai_player.get_best_move(self.game.board)
        
        self.board_view.highlight_selected(*start_pos)
        self.status_label.configure(
            text=f"AI moving {chr(start_pos[0]+97)}{start_pos[1]+1} to {chr(end_pos[0]+97)}{end_pos[1]+1}"
        )
        self.root.update()
        
        self.root.after(500)
        
        self.game.board.move_piece(start_pos, end_pos)
        self.board_view.update(self.game.board)
        
        self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
        self.status_label.configure(
            text=f"{self.game.current_player.capitalize()}'s turn"
        )
        
        if self.game.board.is_checkmate(self.game.current_player):
            winner = 'Black' if self.game.current_player == 'white' else 'White'
            self.show_game_over(winner)