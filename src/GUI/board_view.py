import tkinter as tk
from .piece_view import PieceView

class BoardView:
    def __init__(self, master, board, cell_callback):
        self.master = master
        self.board = board
        self.cell_callback = cell_callback
        
        # Enhanced styling configuration
        self.colors = {
            'light_square': '#E8D0AA',    # Warm light wood
            'dark_square': '#B58863',     # Rich dark wood
            'highlight_selected': '#F7EC75',  # Soft yellow
            'highlight_moves': '#AAD04B',    # Sage green
            'coordinate_text': '#4A4A4A',    # Dark gray
            'border': '#8B4513'             # Dark brown border
        }
        
        # Improved dimensions and spacing
        self.cell_size = 70  # Slightly larger cells
        self.border_width = 20  # Add a border
        self.total_width = 5 * self.cell_size + 2 * self.border_width
        self.total_height = 6 * self.cell_size + 2 * self.border_width
        
        # Create main frame with border
        self.frame = tk.Frame(
            master,
            bd=2,
            relief='ridge',
            bg=self.colors['border']
        )
        self.frame.pack(pady=20, padx=20)
        
        # Create canvas with border
        self.canvas = tk.Canvas(
            self.frame,
            width=self.total_width,
            height=self.total_height,
            bg=self.colors['border'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.piece_view = PieceView(self.canvas)
        self.piece_map = {}
        
        # Draw components
        self.draw_border()
        self.draw_board()
        self.draw_coordinates()
        self.draw_pieces()
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.hover_square = None

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
                
                # Alternate square colors
                color = self.colors['light_square'] if (row + col) % 2 == 0 else self.colors['dark_square']
                
                # Create square with subtle shadow effect
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='',
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
                if not self.board.would_be_in_check(piece.color, (col, row), move)
            ]
            for move_col, move_row in valid_moves:
                self.highlight_square(move_col, move_row, self.colors['highlight_moves'])

    def on_canvas_click(self, event):
        """Handle mouse clicks with improved coordinate calculation."""
        col, row = self.get_square_from_coords(event.x, event.y)
        if 0 <= col < 5 and 0 <= row < 6:
            self.cell_callback(col, row)

    def update(self, board=None):
        """Update the board view."""
        if board:
            self.board = board
        self.canvas.delete('highlight')
        self.draw_pieces()