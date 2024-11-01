import tkinter as tk
from .piece_view import PieceView

class BoardView:
    def __init__(self, master, board, cell_callback):
        self.master = master
        self.board = board
        self.cell_callback = cell_callback
        self.selected_square = None
        self.possible_moves = []
        
        # Create canvas with specific size
        self.cell_size = 60
        self.canvas = tk.Canvas(master, width=5*self.cell_size, height=6*self.cell_size, bg='white')
        self.canvas.pack(pady=10)
        
        self.piece_view = PieceView(self.canvas)
        self.piece_map = {}
        
        self.draw_board()
        self.draw_pieces()
        
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def draw_board(self):
        colors = ['#DDB88C', '#A66D4F']  # Light and dark wood colors
        
        for row in range(6):
            for col in range(5):
                x1 = col * self.cell_size
                y1 = (5 - row) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = colors[(row + col) % 2]
                
                # Store rectangle ID for highlighting
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                
                # Add coordinates
                if col == 0:
                    self.canvas.create_text(x1+10, y1+10, text=str(row+1), font=('Arial', 8))
                if row == 5:  # Changed from 0 to show at bottom
                    self.canvas.create_text(x1+self.cell_size/2, y2-10, text=chr(col+97), font=('Arial', 8))

    def highlight_square(self, col, row, color='yellow'):
        x1 = col * self.cell_size
        y1 = (5 - row) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        # Create highlight with transparency
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple='gray50', tags='highlight')

    def highlight_moves(self, moves):
        # Clear previous highlights
        self.canvas.delete('highlight')
        
        # Highlight possible moves
        for col, row in moves:
            self.highlight_square(col, row, 'light green')

    def get_square_from_coords(self, x, y):
        col = x // self.cell_size
        row = 5 - (y // self.cell_size)  # Convert to board coordinates
        return col, row

    def draw_pieces(self):
        # Clear existing pieces
        self.canvas.delete('piece')
        self.piece_map.clear()
        
        for row in range(6):
            for col in range(5):
                piece = self.board.board[row][col]
                if piece:
                    x = col * self.cell_size + self.cell_size // 2
                    y = (5 - row) * self.cell_size + self.cell_size // 2
                    piece_image = self.piece_view.create_piece(piece, x, y)
                    if piece_image:
                        self.piece_map[piece] = piece_image

    def on_canvas_click(self, event):
        col, row = self.get_square_from_coords(event.x, event.y)
        
        if 0 <= col < 5 and 0 <= row < 6:
            self.cell_callback(col, row)

    def update(self, board):
        self.board = board
        # Clear highlights
        self.canvas.delete('highlight')
        # Redraw pieces
        self.draw_pieces()

    def highlight_selected(self, col, row):
        # Clear previous highlights
        self.canvas.delete('highlight')
        # Highlight selected square
        self.highlight_square(col, row, 'yellow')
        
        # Get and highlight possible moves
        piece = self.board.board[row][col]
        if piece:
            moves = piece.get_possible_moves(self.board)
            for move_col, move_row in moves:
                self.highlight_square(move_col, move_row, 'light green')