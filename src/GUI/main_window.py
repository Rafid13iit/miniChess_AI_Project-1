import tkinter as tk
from tkinter import ttk, messagebox
from .game_setup import GameSetupDialog
from .board_view import BoardView
from ..game import MinichessGame

class MainWindow:
    def __init__(self, root):
        """
        Initialize the main application window.

        This method initializes the main application window, configures the
        root window, sets up the application styles, and displays the start
        screen.

        Parameters:
            root (tkinter.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("MiniChess")
        self.game = None
        self.selected_piece = None

        # Configure root window
        """
        Configure the root window of the application.
        """
        self.root.configure(bg='#F5F5F7')

        # Center the window
        self.center_window(1000, 700)

        # Configure styles
        self.setup_styles()

        # Start screen
        self.start_screen()



    def setup_styles(self):
        """
        Configure ttk styles for the application.

        This function configures the ttk styles for the application. This
        includes setting the font, foreground color, background color, and
        padding for various widgets.

        The styles configured are:

        * Title.TLabel: The title label that appears at the top of the
          main menu and game screens. This label has a bold font with a
          size of 36 and a foreground color of #2C3E50 (a dark blue-gray
          color). The background color is #f0f0f0 (a light gray color) and
          the padding is 20 pixels.
        * GameButton.TButton: The buttons that appear in the main menu
          and game screens. These buttons have a font size of 14 and a
          padding of 10 pixels.
        * Status.TLabel: The status label that appears at the bottom of
          the game screen. This label has a font size of 12 and a
          background color of #f0f0f0 (a light gray color). The padding is
          5 pixels.
        * GameInfo.TFrame: The frame that contains the game information
          (e.g. the number of moves made, the current player, etc.). This
          frame has a background color of #f0f0f0 (a light gray color).
        * MainMenu.TFrame: The frame that contains the main menu. This
          frame has a background color of #f0f0f0 (a light gray color).
        * InGame.TFrame: The frame that contains the game board. This
          frame has a background color of #f0f0f0 (a light gray color).
        """
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
        """
        Center the window on the screen.

        This method calculates the position of the window such that it
        is centered on the screen. The width and height parameters
        specify the size of the window that should be centered.

        The method first gets the width and height of the screen in
        pixels. It then calculates the x and y coordinates of the
        window by subtracting half of the width and height from the
        screen width and height, respectively. Finally, it sets the
        geometry of the window using the calculated x and y
        coordinates and the specified width and height.
        """
        # Get the width and height of the screen in pixels
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates of the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the geometry of the window
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def start_screen(self):
        """Create the main menu screen"""
        # Clear all existing widgets from the root window to prepare for the main menu
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a main frame with the 'MainMenu.TFrame' style to hold the menu content
        main_frame = ttk.Frame(self.root, style='MainMenu.TFrame')
        main_frame.pack(expand=True, fill='both')
        
        # Create a frame for the title/logo section of the main menu
        title_frame = ttk.Frame(main_frame, style='MainMenu.TFrame')
        title_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add a label to the title frame with the application name styled as 'Title.TLabel'
        ttk.Label(title_frame,
                  text="♔  MiniChess ♞",
                  style='Title.TLabel').pack(expand=True)
        
        # Create a frame for holding the buttons in the main menu
        button_frame = ttk.Frame(main_frame, style='MainMenu.TFrame')
        button_frame.pack(expand=True, pady=20)
        
        # Add a "New Game" button to the button frame, styled as 'GameButton.TButton'
        # The button triggers the setup_game method when clicked
        new_game_btn = ttk.Button(button_frame,
                                  text="New Game",
                                  style='GameButton.TButton',
                                  command=self.setup_game,
                                  width=20)
        new_game_btn.pack(pady=10)
        
        # Add a "Quit" button to the button frame, styled as 'GameButton.TButton'
        # The button closes the application when clicked
        quit_btn = ttk.Button(button_frame,
                              text="Quit",
                              style='GameButton.TButton',
                              command=self.root.quit,
                              width=20)
        quit_btn.pack(pady=10)

    def setup_game(self):
        """Open game setup dialog"""
        # Create a new GameSetupDialog (which is a custom Tkinter dialog window)
        # The dialog window is a child of the main application window
        setup_dialog = GameSetupDialog(self.root)
        
        # Wait until the dialog window is closed
        # This is necessary because the dialog window is opened in the main thread
        # and the main application window needs to wait until the dialog window is closed
        # before continuing
        self.root.wait_window(setup_dialog.window)
        
        # Call the start_game method on the dialog window
        # This method returns a new MinichessGame object
        self.game = setup_dialog.start_game()
        
        # If the game was successfully started, start the game UI
        if self.game:
            self.start_game_ui()

    def start_game_ui(self):
        """Initialize the game interface
        
        This function is responsible for setting up the game interface. It clears
        the main window of any existing widgets, creates a main frame for the game
        interface, and then adds subframes for the game information, menu bar, and
        the board view.
        
        """
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
        
        # Menu bar buttons
        # These buttons are not actually functional yet
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
        """
        Display game over dialog with animations
        
        This function displays a new dialog window when the game is over.
        The dialog window is a child of the main application window and
        is centered on the screen. The dialog window displays the winning
        player and provides two buttons: "New Game" and "Main Menu".

        The "New Game" button triggers the setup_game method when clicked,
        which opens a new game setup dialog. The "Main Menu" button triggers
        the start_screen method when clicked, which clears the main window of
        any existing widgets and creates a new main menu screen.
        """
        # Create a new dialog window
        # The dialog window is a child of the main application window
        dialog = tk.Toplevel(self.root)
        
        # Set the window to be transient (i.e. always on top of the main window)
        # and grab the focus so that the dialog window is the only window that
        # can receive events
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set the background color of the dialog window to #f0f0f0 (a light gray color)
        dialog.configure(bg='#f0f0f0')
        
        # Set the title of the dialog window to "Game Over"
        dialog.title("Game Over")
        
        # Calculate the x and y coordinates of the dialog window
        # The dialog window should be centered on the screen
        dialog_width = 400
        dialog_height = 400
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        
        # Set the geometry of the dialog window
        dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')
        
        # Create a label to display the game over message
        # The label should be styled as 'Title.TLabel'
        ttk.Label(dialog,
                 text="Game Over!",
                 style='Title.TLabel').pack(pady=10)
        
        # Create a label to display the winning player
        # The label should be styled as 'Status.TLabel'
        ttk.Label(dialog,
                 text=f"{winner} wins!",
                 style='Status.TLabel').pack(pady=10)
        
        # Create a frame to hold the buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(expand=True)
        
        # Create a button for starting a new game
        # The button should be styled as 'GameButton.TButton'
        # The button should trigger the setup_game method when clicked
        ttk.Button(button_frame,
                  text="New Game",
                  command=lambda: [dialog.destroy(), self.setup_game()],
                  style='GameButton.TButton').pack(side='left', padx=5)
        
        # Create a button for returning to the main menu
        # The button should be styled as 'GameButton.TButton'
        # The button should trigger the start_screen method when clicked
        ttk.Button(button_frame,
                  text="Main Menu",
                  command=lambda: [dialog.destroy(), self.start_screen()],
                  style='GameButton.TButton').pack(side='left', padx=5)

    def on_cell_clicked(self, col, row):
        """
        Handle cell clicks on the board. This method is responsible for handling
        all game logic related to player moves.

        The method first checks if an AI player is currently playing. If an AI
        player is playing, the method simply returns without doing anything else.

        If an AI player is not playing, the method checks if a piece is currently
        selected. If a piece is not selected, the method checks if the cell that
        was clicked contains a piece that belongs to the current player. If the
        cell contains a piece that belongs to the current player, the piece is
        selected and the board view is updated to highlight the selected piece.

        If a piece is already selected, the method checks if the cell that was
        clicked is the same as the cell that contains the selected piece. If the
        cells are the same, the selected piece is deselected and the board view
        is updated to reflect the deselection.

        If the cells are not the same, the method attempts to move the selected
        piece to the cell that was clicked. If the move is successful, the board
        view is updated to reflect the move and the selected piece is deselected.

        If the move is not successful, the method checks if the cell that was
        clicked contains a piece that belongs to the current player. If the cell
        contains a piece that belongs to the current player, the piece is selected
        and the board view is updated to highlight the selected piece.

        If the cell does not contain a piece that belongs to the current player,
        the method deselects the currently selected piece and updates the board
        view to reflect the deselection.

        Finally, the method checks if the game is over by checking if the current
        player is in checkmate. If the game is over, the method displays a game
        over dialog with the winner of the game.
        """
        # Check if an AI player is currently playing
        if self.game.players[self.game.current_player]:
            return
        # Get the piece at the cell that was clicked
        piece = self.game.board.board[row][col]
        
        # Check if a piece is currently selected
        if not self.selected_piece:
            # Check if the cell contains a piece that belongs to the current player
            if piece and piece.color == self.game.current_player:
                # Select the piece
                self.selected_piece = (col, row)
                # Update the board view to highlight the selected piece
                self.board_view.highlight_selected(col, row)
                # Update the status label to show the selected piece
                self.status_label.configure(
                    text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}"
                )
        else:
            # Get the coordinates of the currently selected piece
            start_col, start_row = self.selected_piece
            
            # Check if the cell that was clicked is the same as the cell that contains the selected piece
            if (col, row) == (start_col, start_row):
                # Deselect the piece
                self.selected_piece = None
                # Update the board view to reflect the deselection
                self.board_view.update(self.game.board)
                # Update the status label to show that it is the current player's turn
                self.status_label.configure(
                    text=f"{self.game.current_player.capitalize()}'s turn"
                )
                return
            
            # Attempt to move the selected piece to the cell that was clicked
            if self.game.board.move_piece(self.selected_piece, (col, row)):
                # Update the board view to reflect the move
                self.board_view.update(self.game.board)
                # Deselect the piece
                self.selected_piece = None
                
                # Update the current player
                self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
                # Update the status label to show that it is the current player's turn
                self.status_label.configure(
                    text=f"{self.game.current_player.capitalize()}'s turn"
                )
                
                # Check if the game is over
                if self.game.board.is_checkmate(self.game.current_player):
                    # Get the winner of the game
                    winner = 'Black' if self.game.current_player == 'white' else 'White'
                    # Display a game over dialog with the winner
                    self.show_game_over(winner)
                    return
                
                # If the current player is an AI player, play their turn
                if self.game.players[self.game.current_player]:
                    # Wait for 500 milliseconds before playing the AI player's turn
                    self.root.after(500, self.play_ai_turn)
            else:
                # Check if the cell contains a piece that belongs to the current player
                if piece and piece.color == self.game.current_player:
                    # Select the piece
                    self.selected_piece = (col, row)
                    # Update the board view to highlight the selected piece
                    self.board_view.highlight_selected(col, row)
                    # Update the status label to show the selected piece
                    self.status_label.configure(
                        text=f"Selected {piece.__class__.__name__} at {chr(col+97)}{row+1}"
                    )
                else:
                    # Deselect the piece
                    self.selected_piece = None
                    # Update the board view to reflect the deselection
                    self.board_view.update(self.game.board)
                    # Update the status label to show that it is the current player's turn
                    self.status_label.configure(
                        text=f"Invalid move. {self.game.current_player.capitalize()}'s turn"
                    )

    def play_ai_turn(self):
        """Handle AI player moves"""
        
        # Get the AI player for the current turn
        ai_player = self.game.players[self.game.current_player]
        
        # Determine the best move for the AI player using the current game board
        start_pos, end_pos = ai_player.get_best_move(self.game.board)
        
        # Highlight the starting position of the AI's selected move on the board
        self.board_view.highlight_selected(*start_pos)
        
        # Update the status label to indicate the AI's move
        self.status_label.configure(
            text=f"AI moving {chr(start_pos[0]+97)}{start_pos[1]+1} to {chr(end_pos[0]+97)}{end_pos[1]+1}"
        )
        
        # Refresh the UI to immediately show the updates
        self.root.update()
        
        # Introduce a delay before executing the move to make the AI's decision visible
        self.root.after(500)
        
        # Execute the move on the game board
        self.game.board.move_piece(start_pos, end_pos)
        
        # Update the board view to reflect the new state of the game board
        self.board_view.update(self.game.board)
        
        # Switch the current player to the other player (toggle between 'white' and 'black')
        self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
        
        # Update the status label to indicate the next player's turn
        self.status_label.configure(
            text=f"{self.game.current_player.capitalize()}'s turn"
        )
        
        # Check if the move resulted in a checkmate
        if self.game.board.is_checkmate(self.game.current_player):
            # Determine the winner based on the current player
            winner = 'Black' if self.game.current_player == 'white' else 'White'
            # Display a game over dialog with the winner
            self.show_game_over(winner)
