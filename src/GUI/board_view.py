# board_view.py
import tkinter as tk
import time
import pygame.mixer
from .piece_view import PieceView
from .board_themes import ChessBoardThemes

class BoardView:
    def __init__(self, master, board, cell_callback):
        """
        Construct a BoardView widget

        :param master: The parent widget
        :param board: The board object from the game
        :param cell_callback: A callback function for when a cell is clicked
        """
        self.master = master
        self.board = board
        self.cell_callback = cell_callback

        # Initialize pygame mixer for sounds
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound('assets/move.wav')
        self.capture_sound = pygame.mixer.Sound('assets/capture.wav')

        # Initialize themes
        self.theme_manager = ChessBoardThemes()

        # Create main container frame
        self.container = tk.Frame(master)
        self.container.pack(pady=30, padx=30)

        # Create left frame for chess board
        self.frame = tk.Frame(
            self.container,
            bd=2,
            relief='ridge'
        )
        self.frame.pack(side=tk.LEFT, padx=(0, 20))

        # Create control frame for undo/redo buttons
        self.control_frame = tk.Frame(self.container)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0, 20))

        # Add undo/redo buttons
        self.undo_button = tk.Button(
            self.control_frame,
            text="Undo",
            command=self.undo_move,
            font=('Helvetica', 12),
            width=10,
            pady=5
        )
        self.undo_button.pack(pady=(0, 5))

        self.redo_button = tk.Button(
            self.control_frame,
            text="Redo",
            command=self.redo_move,
            font=('Helvetica', 12),
            width=10,
            pady=5
        )
        self.redo_button.pack()

        # Store moves that were undone for redo functionality
        self.undone_moves = []

        # Create right frame for theme selection
        self.theme_frame = tk.Frame(self.container)
        self.theme_frame.pack(side=tk.LEFT, fill=tk.Y, pady=20)

        # Add theme selector label
        self.theme_label = tk.Label(
            self.theme_frame,
            text="Board Theme",
            font=('Helvetica', 12, 'bold'),
            pady=10
        )
        self.theme_label.pack()

        # Create frames for two columns
        self.column_left = tk.Frame(self.theme_frame)
        self.column_left.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.column_right = tk.Frame(self.theme_frame)
        self.column_right.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Create theme buttons with preview swatches in two columns
        self.theme_buttons = {}
        self.current_theme = tk.StringVar(value='vintage_walnut')

        # Loop through themes and place in two columns
        for i, (theme_id, theme_name) in enumerate(self.theme_manager.get_all_themes()):
            # Alternate between left and right columns
            target_column = self.column_left if i % 2 == 0 else self.column_right

            theme_container = tk.Frame(target_column)
            theme_container.pack(pady=5, fill=tk.X)

            # Create small preview canvas
            preview = tk.Canvas(
                theme_container,
                width=40,
                height=40,
                highlightthickness=1,
                highlightbackground='#CCCCCC'
            )
            preview.pack(side=tk.LEFT, padx=(0, 5))

            # Draw preview squares
            colors = self.theme_manager.get_theme(theme_id)
            preview.create_rectangle(0, 0, 20, 20, fill=colors['light_square'], outline='')
            preview.create_rectangle(20, 0, 40, 20, fill=colors['dark_square'], outline='')
            preview.create_rectangle(0, 20, 20, 40, fill=colors['dark_square'], outline='')
            preview.create_rectangle(20, 20, 40, 40, fill=colors['light_square'], outline='')

            # Create radio button
            rb = tk.Radiobutton(
                theme_container,
                text=theme_name,
                value=theme_id,
                variable=self.current_theme,
                command=self.on_theme_change,
                font=('Helvetica', 10),
                anchor='w'
            )
            rb.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.theme_buttons[theme_id] = rb

        # Set default theme
        self.colors = self.theme_manager.get_theme(self.current_theme.get())

        # Enhanced dimensions
        self.cell_size = 70
        self.border_width = 20
        self.total_width = 5 * self.cell_size + 2 * self.border_width
        self.total_height = 6 * self.cell_size + 2 * self.border_width

        # Create canvas with professional styling
        self.canvas = tk.Canvas(
            self.frame,
            width=self.total_width,
            height=self.total_height,
            highlightthickness=0
        )
        self.canvas.pack()

        self.piece_view = PieceView(self.canvas)
        self.piece_map = {}
        self.selected_piece = None
        self.last_move = None

        # Initialize board components
        self.draw_border()
        self.draw_board()
        self.draw_coordinates()
        self.draw_pieces()

        # Event bindings
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.hover_square = None

        # Initialize undo/redo button states
        self.update_undo_redo_buttons()

    def undo_move(self):
        """Undo the last move."""
        # Check if there is any move in the move history
        if self.board.move_history:
            # Retrieve the last move from the move history for potential redo
            last_move = self.board.move_history[-1]
            # Save the last move to the undone moves stack
            self.undone_moves.append(last_move)
            
            # Call the board's method to undo the last move
            self.board.undo_last_move()
            
            # Update the board display to reflect the undone move
            if self.board.move_history:
                # If there are moves left in the history, highlight the new last move
                last_remaining = self.board.move_history[-1]
                self.last_move = (last_remaining['start'], last_remaining['end'])
            else:
                # If no moves are left in the history, clear the last move highlight
                self.last_move = None
            
            # Refresh the board view with the updated state
            self.update()
            # Update the states of undo and redo buttons
            self.update_undo_redo_buttons()
            
            # Play move sound effect to indicate an action was performed
            self.play_sound(is_capture=False)

    def redo_move(self):
        """Redo the previously undone move.

        This function is responsible for re-executing a move that was previously undone.
        It retrieves the last undone move from the `undone_moves` list, executes it on the board,
        updates the board display, and updates the states of the undo/redo buttons.

        If there are no undone moves, the function does nothing.
        """
        if self.undone_moves:
            # Retrieve the last undone move from the list
            move = self.undone_moves.pop()

            # Extract the start and end positions of the move
            start_pos = move['start']
            end_pos = move['end']

            # Execute the move on the board
            self.board.move_piece(start_pos, end_pos)

            # Update the board display to reflect the re-executed move
            self.last_move = (start_pos, end_pos)
            self.update()

            # Update the states of the undo/redo buttons
            self.update_undo_redo_buttons()

            # Play an appropriate sound effect to indicate an action was performed
            self.play_sound(is_capture=bool(move['captured']))

    def update_undo_redo_buttons(self):
        """
        Update the enabled/disabled state of undo/redo buttons based on the state of the game.

        This function is called whenever the game state changes, such as when a move is made or undone.
        It determines whether the undo and redo buttons should be enabled or disabled, based on the following rules:

        - The undo button should be enabled if there is at least one move in the move history.
        - The redo button should be enabled if there is at least one move in the undone moves list.
        - Both buttons should be disabled if there are no moves in either the move history or the undone moves list.

        This function is essential for maintaining the correct state of the undo/redo buttons, which in turn helps to
        prevent invalid moves from being made.
        """
        # Check if there are any moves in the move history
        has_move_history = bool(self.board.move_history)
        # Check if there are any moves in the undone moves list
        has_undone_moves = bool(self.undone_moves)

        # Enable or disable the undo button based on the move history
        self.undo_button.configure(state=tk.NORMAL if has_move_history else tk.DISABLED)
        # Enable or disable the redo button based on the undone moves list
        self.redo_button.configure(state=tk.NORMAL if has_undone_moves else tk.DISABLED)

    def on_theme_change(self):
        """
        Handle theme selection change.

        This function is called whenever the theme selection dropdown is changed.
        It retrieves the newly selected theme from the StringVar associated with
        the dropdown, retrieves the corresponding colors from the theme manager,
        and then redraws the entire board using the new colors.

        The redraw is done by calling the `redraw_board` method, which clears the
        canvas and redraws all the board components (border, board, coordinates,
        and pieces) using the new colors.
        """
        new_theme = self.current_theme.get()
        self.colors = self.theme_manager.get_theme(new_theme)
        self.redraw_board()


    def play_sound(self, is_capture=False):
        """
        Play sound effects for moves and captures.

        This function plays a sound effect whenever a move is made. If a piece is
        captured, a different sound effect is played. The sound effect is played
        and then stopped after the duration of the sound. This ensures that the
        sound effect is played only once and then stops, preventing continuous
        sound effects from overlapping.

        Parameters
        ----------
        is_capture : bool, optional
            If `True`, the capture sound effect is played. Otherwise, the regular
            move sound effect is played. Defaults to `False`.

        """
        if is_capture:
            # Play the capture sound effect if a piece is captured
            self.capture_sound.play()
        else:
            # Play the regular move sound effect for regular moves
            self.move_sound.play()

        # Delay for the duration of the sound, then stop it
        time.sleep(self.move_sound.get_length())
        # Stop the sound after playing it
        self.stop_sound()

    def stop_sound(self):
        """Stop any sound that's playing."""
        pygame.mixer.stop()


    def redraw_board(self):
        """
        Redraw the entire board with the current theme.

        This function updates the visual appearance of the chessboard by applying the
        selected theme colors. It ensures that the entire board is redrawn with the
        current configuration, including the border, board squares, coordinates, and pieces.

        The function also checks if there was a last move made and highlights it on the board.
        """
        # Set the background color of the frame and canvas to the border color of the current theme
        self.frame.configure(bg=self.colors['border'])
        self.canvas.configure(bg=self.colors['border'])
        
        # Draw the decorative border around the board using the current theme
        self.draw_border()
        
        # Render the 5x6 chess board squares with alternating colors based on the current theme
        self.draw_board()
        
        # Add coordinates (numbers and letters) around the board for reference
        self.draw_coordinates()
        
        # Draw all the chess pieces on the board in their current positions
        self.draw_pieces()
        
        # If a move has been made, highlight the squares involved in the last move
        if self.last_move:
            self.highlight_last_move(*self.last_move)

    def draw_border(self):
        """
        Draw decorative border around the board.

        The border is a rectangle that surrounds the entire board, including the
        coordinates and the chess pieces. The border is drawn with a width of 0
        (i.e., no border), and the color of the border is set to the "border"
        color of the current theme.

        This code creates a canvas item of type "rectangle" with the following
        properties:

        * x1 and y1 coordinates of the top-left corner of the rectangle
        * x2 and y2 coordinates of the bottom-right corner of the rectangle
        * fill color of the border (set to the "border" color of the current theme)
        * width of 0 (i.e., no border)

        The resulting border is a solid rectangle that surrounds the entire board.
        """

        """Draw decorative border around the board."""
        self.canvas.create_rectangle(
            0, 0, self.total_width, self.total_height,
            fill=self.colors['border'],
            width=0
        )

    def draw_board(self):
        """
        Draw the 5x6 chess board with enhanced visuals.

        This code draws a 5x6 chess board with alternating light and dark squares.
        The board is drawn with improved visuals, including a border and shaded squares.
        """
        # Iterate over each row and column of the board
        for row in range(6):
            for col in range(5):
                # Calculate the coordinates of the top-left and bottom-right corners of the square
                x1 = col * self.cell_size + self.border_width
                y1 = (5 - row) * self.cell_size + self.border_width
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Determine the color of the square based on its position
                # If the sum of the row and column numbers is even, the square is light
                # Otherwise, the square is dark
                color = self.colors['light_square'] if (row + col) % 2 == 0 else self.colors['dark_square']
                
                # Create a canvas item of type "rectangle" with the following properties:
                # * x1 and y1 coordinates of the top-left corner of the square
                # * x2 and y2 coordinates of the bottom-right corner of the square
                # * fill color of the square (light or dark)
                # * outline color of the square (border color)
                # * tags for the square (square_{col}_{row})
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=self.colors['border'],
                    tags=f'square_{col}_{row}'
                )

    def draw_coordinates(self):
        """
        Draw board coordinates with improved styling.

        This function draws the row numbers (1-6) and column letters (a-e) around the
        chess board. The coordinates are drawn with a bold font and a contrasting
        color to make them stand out.

        The coordinates are drawn on all four sides of the board, with the row numbers
        on the left and right sides, and the column letters on the top and bottom
        sides.
        """
        font = ('Helvetica', 12, 'bold')
        
        # Draw row numbers (1-6) on the left and right sides
        for row in range(6):
            y = (5 - row) * self.cell_size + self.cell_size/2 + self.border_width
            # Left side
            self.canvas.create_text(
                # Calculate the x-coordinate of the left side of the board
                self.border_width/2,
                y,
                # Set the text to the row number
                text=str(row + 1),
                # Set the font to a bold font
                font=font,
                # Set the text color to the contrasting color
                fill=self.colors['coordinate_text']
            )
            # Right side
            self.canvas.create_text(
                # Calculate the x-coordinate of the right side of the board
                self.total_width - self.border_width/2,
                y,
                # Set the text to the row number
                text=str(row + 1),
                # Set the font to a bold font
                font=font,
                # Set the text color to the contrasting color
                fill=self.colors['coordinate_text']
            )
        
        # Draw column letters (a-e) on the top and bottom sides
        for col in range(5):
            x = col * self.cell_size + self.cell_size/2 + self.border_width
            # Bottom
            self.canvas.create_text(
                x,
                # Calculate the y-coordinate of the bottom of the board
                self.total_height - self.border_width/2,
                # Set the text to the column letter
                text=chr(97 + col),
                # Set the font to a bold font
                font=font,
                # Set the text color to the contrasting color
                fill=self.colors['coordinate_text']
            )
            # Top
            self.canvas.create_text(
                x,
                # Calculate the y-coordinate of the top of the board
                self.border_width/2,
                # Set the text to the column letter
                text=chr(97 + col),
                # Set the font to a bold font
                font=font,
                # Set the text color to the contrasting color
                fill=self.colors['coordinate_text']
            )

    def highlight_square(self, col, row, color, alpha=0.3):
        """
        Highlight a square on the board with an improved visual effect.

        The improved visual effect is a semi-transparent gray and white
        checkerboard pattern. This is achieved by using the stipple option
        of the canvas's create_rectangle method.

        This method takes four parameters:

        - col: The column number of the square to highlight (0-4)
        - row: The row number of the square to highlight (0-5)
        - color: The color of the highlight (should be a valid color name)
        - alpha: The alpha value of the highlight (0.0-1.0), default is 0.3

        The method returns the item id of the highlight rectangle.
        """
        # Calculate the x and y coordinates of the top-left corner of the square
        x1 = col * self.cell_size + self.border_width
        y1 = (5 - row) * self.cell_size + self.border_width

        # Calculate the x and y coordinates of the bottom-right corner of the square
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Create a rectangle with the calculated coordinates, fill it with the given color
        # and set the stipple pattern to a gray and white checkerboard
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            stipple='gray50',
            tags='highlight'  # Add the highlight rectangle to the "highlight" tag
        )

    def get_square_from_coords(self, x, y):
        """
        Convert canvas coordinates to board coordinates, taking into account the border offset.

        This method takes two parameters:

        - x: The x-coordinate on the canvas
        - y: The y-coordinate on the canvas

        It returns a tuple of two values:

        - col: The column number of the corresponding square on the board (0-4)
        - row: The row number of the corresponding square on the board (0-5)

        The method first subtracts the border width from the x and y coordinates to
        get the coordinates relative to the board area. Then it calculates the column
        number by doing integer division of the x-coordinate by the cell size. The row
        number is calculated by subtracting the result of the integer division of the
        y-coordinate by the cell size from 5 (since the board is drawn upside-down).
        """
        # Subtract the border width from the x and y coordinates to get the coordinates
        # relative to the board area
        x = x - self.border_width
        y = y - self.border_width

        # Calculate the column number by doing integer division of the x-coordinate by
        # the cell size
        col = x // self.cell_size

        # Calculate the row number by subtracting the result of the integer division of
        # the y-coordinate by the cell size from 5 (since the board is drawn upside-down)
        row = 5 - (y // self.cell_size)

        # Return the column and row numbers as a tuple
        return col, row


    def draw_pieces(self):
        """
        Draw all pieces with adjusted positioning.

        This method first clears all piece images from the canvas by deleting
        all items with the 'piece' tag. It also clears the piece map, which is
        a dictionary that maps each piece to its corresponding image item id.

        Then it iterates over all squares on the board (0-4 for columns and 0-5
        for rows). For each square, it gets the piece at that square from the
        board. If there is a piece at that square, it calculates the x and y
        coordinates of the piece by multiplying the column and row numbers by
        the cell size, adding half the cell size to center the piece, and adding
        the border width to account for the border offset.

        Finally, it creates a piece image using the PieceView class and adds it
        to the canvas at the calculated coordinates. The piece image is then
        added to the piece map dictionary.
        """
        self.canvas.delete('piece')
        self.piece_map.clear()
        
        for row in range(6):
            for col in range(5):
                piece = self.board.get_piece((col, row))
                if piece:
                    x = col * self.cell_size + self.cell_size // 2 + self.border_width
                    y = (5 - row) * self.cell_size + self.cell_size // 2 + self.border_width
                    piece_image = self.piece_view.create_piece(piece, x, y)
                    if piece_image:
                        self.piece_map[piece] = piece_image

    def on_mouse_move(self, event):
        """
        Handle mouse hover effects.

        This method is responsible for changing the mouse cursor based on whether
        the mouse is hovering over a square on the board or not, and whether the
        piece on that square is of the current player's color.

        It takes an event argument, which is a Tkinter event object that contains
        information about the mouse event, such as the x and y coordinates of the
        mouse cursor.

        It first calculates the column and row numbers of the square that the
        mouse is currently hovering over by calling the get_square_from_coords
        method.

        If the column and row numbers are within the valid range of 0 to 4 for
        columns and 0 to 5 for rows, it checks if the mouse is hovering over a
        different square than it was previously. If it is, it updates the
        hover_square attribute to keep track of the currently hovered square.

        Then it gets the piece at the currently hovered square from the board
        using the get_piece method.

        If the piece is not None and its color is the same as the current player's
        color, it sets the mouse cursor to a hand2 cursor, which is a cursor that
        indicates that the user can drag something. Otherwise, it sets the mouse
        cursor to an arrow cursor, which is the default cursor.

        If the column and row numbers are not within the valid range, it sets the
        mouse cursor to an arrow cursor and sets the hover_square attribute to
        None to indicate that the mouse is not hovering over any square.
        """
        col, row = self.get_square_from_coords(event.x, event.y)
        if 0 <= col < 5 and 0 <= row < 6:
            if (col, row) != self.hover_square:
                self.hover_square = (col, row)
                piece = self.board.get_piece((col, row))
                if piece and piece.color == self.board.current_turn:
                    self.canvas.configure(cursor='hand2')
                else:
                    self.canvas.configure(cursor='arrow')
        else:
            self.canvas.configure(cursor='arrow')
            self.hover_square = None

    def highlight_moves(self, moves):
        """
        Highlight possible moves with enhanced visuals.
        
        This method highlights each square on the board where a piece can move.
        It does so by first removing any existing highlights and then drawing
        new highlights on the specified squares.

        :param moves: A list of tuples, where each tuple contains the column and
                      row numbers of a square to be highlighted.
        """
        # Remove all existing highlight rectangles from the canvas to avoid
        # overlapping highlights.
        self.canvas.delete('highlight')

        # Iterate over each move in the list of moves.
        for col, row in moves:
            # Highlight the square at the given column and row. The color used
            # for highlighting is specified in the 'highlight_moves' color setting.
            self.highlight_square(col, row, self.colors['highlight_moves'])

    def highlight_selected(self, col, row):
        """Highlight selected square and possible moves with improved visuals."""
        self.canvas.delete('highlight')
        self.highlight_square(col, row, self.colors['highlight_selected'])
        
        piece = self.board.get_piece((col, row))
        if piece and piece.color == self.board.current_turn:
            moves = piece.get_possible_moves(self.board)
            valid_moves = [
                move for move in moves 
                if not self.board.would_be_in_check(piece.color, (col, row), move)]
            for move_col, move_row in valid_moves:
                self.highlight_square(move_col, move_row, self.colors['highlight_moves'])


    def on_canvas_click(self, event):
        """Handle mouse clicks with piece movement, sound effects, and callback functionality."""

        # Get the column and row from the click coordinates
        col, row = self.get_square_from_coords(event.x, event.y)
        if not (0 <= col < 5 and 0 <= row < 6):
            # If the click is outside the board, don't do anything
            return

        # If no piece is selected
        if self.selected_piece is None:
            piece = self.board.get_piece((col, row))
            if piece and piece.color == self.board.current_turn:
                # Select the piece
                self.selected_piece = (col, row)
                self.highlight_selected(col, row)
                # Trigger callback when selecting a piece
                self.cell_callback(col, row)
        # If a piece is already selected
        else:
            # Get the from and to positions
            from_pos = self.selected_piece
            to_pos = (col, row)

            # Get the piece and its valid moves
            piece = self.board.get_piece(from_pos)
            valid_moves = []
            if piece:
                moves = piece.get_possible_moves(self.board)
                valid_moves = [
                    move for move in moves
                    if not self.board.would_be_in_check(piece.color, from_pos, move)
                ]

            # If the clicked square is a valid move
            if to_pos in valid_moves:
                # Trigger callback before executing the move
                self.cell_callback(col, row)

                # Clear the redo stack when a new move is made
                self.undone_moves.clear()

                # Execute the move
                captured_piece = self.board.get_piece(to_pos)
                self.board.move_piece(from_pos, to_pos)

                # Play appropriate sound
                # self.play_sound(is_capture=bool(captured_piece))
                self.play_sound(is_capture=False)

                # Update display and game state
                self.last_move = (from_pos, to_pos)
                self.selected_piece = None
                self.update()

                # Update undo/redo button states
                self.update_undo_redo_buttons()
            else:
                # If clicked on another own piece, select it instead
                new_piece = self.board.get_piece(to_pos)
                if new_piece and new_piece.color == self.board.current_turn:
                    self.selected_piece = to_pos
                    self.highlight_selected(col, row)
                    # Trigger callback when selecting a new piece
                    self.cell_callback(col, row)
                else:
                    self.selected_piece = None
                    self.canvas.delete('highlight')
                    # Trigger callback for deselection
                    self.cell_callback(col, row)

        # If the last move resulted in a check, we might want to highlight it
        if self.board.is_in_check(self.board.current_turn):
            # You could add visual feedback for check here
            pass

    def highlight_last_move(self, from_pos, to_pos):
        """
        Highlight the last move made on the board.

        This method takes two parameters, `from_pos` and `to_pos`, which are tuples
        representing the starting and ending positions of the last move respectively.

        The method first sets the `last_move` attribute to the tuple of the two positions.

        If both `from_pos` and `to_pos` are truthy, the method then highlights the
        squares at the starting and ending positions with a light gray color using
        the `highlight_square` method. The `alpha` parameter is set to 0.2 to make
        the highlights semi-transparent.
        """
        self.last_move = (from_pos, to_pos)
        if from_pos and to_pos:
            from_col, from_row = from_pos
            to_col, to_row = to_pos
            self.highlight_square(
                from_col, from_row, self.colors['highlight_selected'], alpha=0.2)
            self.highlight_square(
                to_col, to_row, self.colors['highlight_selected'], alpha=0.2)

    def update(self, board=None):
        """
        Update the board view with new board state.

        If the `board` parameter is provided, set the `board` attribute of the
        `BoardView` instance to the provided value. Otherwise, keep the current
        value of the `board` attribute.

        Then, delete all the canvas items with the `highlight` tag, which are
        the highlight squares for the selected piece.

        Finally, redraw the chess pieces on the board using the `draw_pieces`
        method.
        """
        if board:
            self.board = board
        self.canvas.delete('highlight')
        self.draw_pieces()
