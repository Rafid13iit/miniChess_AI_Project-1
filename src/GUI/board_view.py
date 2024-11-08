import tkinter as tk
from .piece_view import PieceView

class BoardView:
    def __init__(self, master, board, cell_callback):
        self.master = master
        self.board = board
        self.cell_callback = cell_callback
        
        # Create canvas for 5x6 board
        self.cell_size = 60
        self.canvas = tk.Canvas(
            master, 
            width=5*self.cell_size, 
            height=6*self.cell_size,
            bg='white'
        )
        self.canvas.pack(pady=10)
        
        self.piece_view = PieceView(self.canvas)
        self.piece_map = {}
        
        self.draw_board()
        self.draw_pieces()
        
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def draw_board(self):
        """Draw the 5x6 chess board with coordinates."""
        colors = ['#DDB88C', '#A66D4F']  # Light and dark wood colors
        
        for row in range(6):
            for col in range(5):
                x1 = col * self.cell_size
                y1 = (5 - row) * self.cell_size  # Flip board vertically
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Alternate colors
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='',
                    tags=f'square_{col}_{row}'
                )
                
                # Add row numbers (1-6)
                if col == 0:
                    self.canvas.create_text(
                        x1 + 10,
                        y1 + 10,
                        text=str(row + 1),
                        font=('Arial', 8),
                        anchor='nw'
                    )
                
                # Add column letters (a-e)
                if row == 5:
                    self.canvas.create_text(
                        x1 + self.cell_size/2,
                        y2 - 10,
                        text=chr(97 + col),  # 'a' through 'e'
                        font=('Arial', 8)
                    )

    def highlight_square(self, col, row, color='yellow'):
        """Highlight a square with the specified color."""
        x1 = col * self.cell_size
        y1 = (5 - row) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            stipple='gray50',
            tags='highlight'
        )

    def get_square_from_coords(self, x, y):
        """Convert canvas coordinates to board coordinates."""
        col = x // self.cell_size
        row = 5 - (y // self.cell_size)  # Convert to board coordinates
        return col, row

    def draw_pieces(self):
        """Draw all pieces on the board."""
        self.canvas.delete('piece')
        self.piece_map.clear()
        
        for row in range(6):
            for col in range(5):
                piece = self.board.get_piece((col, row))
                if piece:
                    x = col * self.cell_size + self.cell_size // 2
                    y = (5 - row) * self.cell_size + self.cell_size // 2
                    piece_image = self.piece_view.create_piece(piece, x, y)
                    if piece_image:
                        self.piece_map[piece] = piece_image

    def highlight_moves(self, moves):
        """Highlight all possible moves."""
        self.canvas.delete('highlight')
        for col, row in moves:
            self.highlight_square(col, row, 'light green')

    def highlight_selected(self, col, row):
        """Highlight selected square and its possible moves."""
        self.canvas.delete('highlight')
        self.highlight_square(col, row, 'yellow')
        
        piece = self.board.get_piece((col, row))
        if piece and piece.color == self.board.current_turn:
            moves = piece.get_possible_moves(self.board)
            # Filter out moves that would result in check
            valid_moves = [
                move for move in moves 
                if not self.board.would_be_in_check(piece.color, (col, row), move)
            ]
            for move_col, move_row in valid_moves:
                self.highlight_square(move_col, move_row, 'light green')

    def on_canvas_click(self, event):
        """Handle mouse clicks on the board."""
        col, row = self.get_square_from_coords(event.x, event.y)
        if 0 <= col < 5 and 0 <= row < 6:
            self.cell_callback(col, row)

    def update(self, board=None):
        """Update the board view with new board state."""
        if board:
            self.board = board
        self.canvas.delete('highlight')
        self.draw_pieces()