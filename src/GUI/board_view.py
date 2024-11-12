# board_view.py
import tkinter as tk
import time
import pygame.mixer
from .piece_view import PieceView
from .board_themes import ChessBoardThemes

class BoardView:
    def __init__(self, master, board, cell_callback):
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
        self.container.pack(pady=20, padx=20)

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
            text="↶ Undo",
            command=self.undo_move,
            font=('Helvetica', 12),
            width=10,
            pady=5
        )
        self.undo_button.pack(pady=(0, 5))

        self.redo_button = tk.Button(
            self.control_frame,
            text="↷ Redo",
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
        if self.board.move_history:
            # Save the last move for potential redo
            last_move = self.board.move_history[-1]
            self.undone_moves.append(last_move)
            
            # Perform the undo
            self.board.undo_last_move()
            
            # Update the display
            if self.board.move_history:
                # If there are still moves in history, show the last one
                last_remaining = self.board.move_history[-1]
                self.last_move = (last_remaining['start'], last_remaining['end'])
            else:
                # If no moves left, clear last move highlight
                self.last_move = None
            
            self.update()
            self.update_undo_redo_buttons()
            
            # Play move sound
            self.play_sound(is_capture=False)

    def redo_move(self):
        """Redo the previously undone move."""
        if self.undone_moves:
            move = self.undone_moves.pop()
            
            # Execute the move
            start_pos = move['start']
            end_pos = move['end']
            
            # Move the piece
            self.board.move_piece(start_pos, end_pos)
            
            # Update the display
            self.last_move = (start_pos, end_pos)
            self.update()
            self.update_undo_redo_buttons()
            
            # Play appropriate sound
            self.play_sound(is_capture=bool(move['captured']))

    def update_undo_redo_buttons(self):
        """Update the enabled/disabled state of undo/redo buttons."""
        self.undo_button.configure(state=tk.NORMAL if self.board.move_history else tk.DISABLED)
        self.redo_button.configure(state=tk.NORMAL if self.undone_moves else tk.DISABLED)

    def on_theme_change(self):
        """Handle theme selection change."""
        new_theme = self.current_theme.get()
        self.colors = self.theme_manager.get_theme(new_theme)
        self.redraw_board()


    def play_sound(self, is_capture=False):
        """Play sound effect for moves and captures."""
        if is_capture:
            self.capture_sound.play()  # Play capture sound if a piece is captured
        else:
            self.move_sound.play()     # Play move sound for regular moves
        
        # Delay for the duration of the sound, then stop it
        time.sleep(self.move_sound.get_length())
        self.stop_sound()

    def stop_sound(self):
        """Stop any sound that's playing."""
        pygame.mixer.stop()


    def redraw_board(self):
        """Redraw the entire board with current theme."""
        self.frame.configure(bg=self.colors['border'])
        self.canvas.configure(bg=self.colors['border'])
        self.draw_border()
        self.draw_board()
        self.draw_coordinates()
        self.draw_pieces()
        if self.last_move:
            self.highlight_last_move(*self.last_move)

    def draw_border(self):
        """Draw decorative border around the board."""
        self.canvas.create_rectangle(
            0, 0, self.total_width, self.total_height,
            fill=self.colors['border'],
            width=0
        )

    def draw_board(self):
        """Draw the 5x6 chess board with enhanced visuals."""
        for row in range(6):
            for col in range(5):
                x1 = col * self.cell_size + self.border_width
                y1 = (5 - row) * self.cell_size + self.border_width
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = self.colors['light_square'] if (row + col) % 2 == 0 else self.colors['dark_square']
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=self.colors['border'],
                    tags=f'square_{col}_{row}'
                )

    def draw_coordinates(self):
        """Draw board coordinates with improved styling."""
        font = ('Helvetica', 12, 'bold')
        
        # Draw row numbers (1-6)
        for row in range(6):
            y = (5 - row) * self.cell_size + self.cell_size/2 + self.border_width
            # Left side
            self.canvas.create_text(
                self.border_width/2,
                y,
                text=str(row + 1),
                font=font,
                fill=self.colors['coordinate_text']
            )
            # Right side
            self.canvas.create_text(
                self.total_width - self.border_width/2,
                y,
                text=str(row + 1),
                font=font,
                fill=self.colors['coordinate_text']
            )
        
        # Draw column letters (a-e)
        for col in range(5):
            x = col * self.cell_size + self.cell_size/2 + self.border_width
            # Bottom
            self.canvas.create_text(
                x,
                self.total_height - self.border_width/2,
                text=chr(97 + col),
                font=font,
                fill=self.colors['coordinate_text']
            )
            # Top
            self.canvas.create_text(
                x,
                self.border_width/2,
                text=chr(97 + col),
                font=font,
                fill=self.colors['coordinate_text']
            )

    def highlight_square(self, col, row, color, alpha=0.3):
        """Highlight a square with improved visual effect."""
        x1 = col * self.cell_size + self.border_width
        y1 = (5 - row) * self.cell_size + self.border_width
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            stipple='gray50',
            tags='highlight'
        )

    def get_square_from_coords(self, x, y):
        """Convert canvas coordinates to board coordinates with border offset."""
        x = x - self.border_width
        y = y - self.border_width
        col = x // self.cell_size
        row = 5 - (y // self.cell_size)
        return col, row

    def draw_pieces(self):
        """Draw all pieces with adjusted positioning."""
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
        """Handle mouse hover effects."""
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
        """Highlight possible moves with enhanced visuals."""
        self.canvas.delete('highlight')
        for col, row in moves:
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
        col, row = self.get_square_from_coords(event.x, event.y)
        if not (0 <= col < 5 and 0 <= row < 6):
            return

        # If no piece is selected
        if self.selected_piece is None:
            piece = self.board.get_piece((col, row))
            if piece and piece.color == self.board.current_turn:
                self.selected_piece = (col, row)
                self.highlight_selected(col, row)
                # Trigger callback when selecting a piece
                self.cell_callback(col, row)
        # If a piece is already selected
        else:
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
        """Highlight the last move made on the board."""
        self.last_move = (from_pos, to_pos)
        if from_pos and to_pos:
            from_col, from_row = from_pos
            to_col, to_row = to_pos
            self.highlight_square(from_col, from_row, self.colors['highlight_selected'], alpha=0.2)
            self.highlight_square(to_col, to_row, self.colors['highlight_selected'], alpha=0.2)

    def update(self, board=None):
        """Update the board view with new board state."""
        if board:
            self.board = board
        self.canvas.delete('highlight')
        self.draw_pieces()