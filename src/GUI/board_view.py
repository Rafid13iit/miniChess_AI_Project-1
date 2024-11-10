import math
import tkinter as tk
from .piece_view import PieceView

class BoardView:
    COLORS = {
        'board_light': '#E8D0AA',  # Warm light wood
        'board_dark': '#B88B4A',   # Rich dark wood
        'highlight_select': '#FFD700',  # Golden yellow
        'highlight_move': '#90EE90',    # Light green
        'highlight_last_move': '#ADD8E6',  # Light blue
        'coordinate_text': '#463E3F',   # Deep gray
        'border': '#2F4858'  # Dark blue-gray
    }

    def __init__(self, master, board, cell_callback):
        self.master = master
        self.board = board
        self.cell_callback = cell_callback
        
        # Calculate optimal cell size based on screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        max_board_width = min(screen_width * 0.8, screen_height * 0.8)  # Use 80% of smaller dimension
        
        # Calculate cell size to fit the board properly
        self.cell_size = int(max_board_width / 7)  # Divide by 7 to account for border and margins
        self.border_size = int(self.cell_size * 0.375)  # Border is 37.5% of cell size
        
        # Create main frame with proper spacing
        self.frame = tk.Frame(
            master,
            bg=self.COLORS['border']
        )
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Calculate exact canvas dimensions
        board_width = 5 * self.cell_size  # 5 columns
        board_height = 6 * self.cell_size  # 6 rows
        total_width = board_width + 2 * self.border_size
        total_height = board_height + 2 * self.border_size
        
        # Create canvas with exact dimensions
        self.canvas = tk.Canvas(
            self.frame,
            width=total_width,
            height=total_height,
            bg=self.COLORS['border'],
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        self.piece_view = PieceView(self.canvas)
        self.piece_map = {}
        self.animations = []
        self.last_move = None
        
        # Center the board in the canvas
        self.board_offset_x = self.border_size
        self.board_offset_y = self.border_size
        
        self.draw_board()
        self.draw_pieces()
        
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.setup_animations()

    def get_square_center(self, col, row):
        """Calculate the exact center position of a square."""
        x = self.board_offset_x + (col + 0.5) * self.cell_size
        y = self.board_offset_y + (5 - row + 0.5) * self.cell_size
        return x, y

    def draw_board(self):
        """Draw the board with precise square positioning."""
        self.draw_coordinates()
        
        for row in range(6):
            for col in range(5):
                x1 = self.board_offset_x + col * self.cell_size
                y1 = self.board_offset_y + (5 - row) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                base_color = self.COLORS['board_light'] if (row + col) % 2 == 0 else self.COLORS['board_dark']
                
                # Draw main square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=base_color,
                    outline='',
                    tags=f'square_{col}_{row}'
                )
                
                # Add subtle inner shadow for depth
                shadow_width = max(1, int(self.cell_size * 0.025))  # Scale shadow with cell size
                self.canvas.create_rectangle(
                    x1 + shadow_width,
                    y1 + shadow_width,
                    x2 - shadow_width,
                    y2 - shadow_width,
                    outline='#000000',
                    width=1,
                    tags=f'shadow_{col}_{row}'
                )

    def draw_coordinates(self):
        """Draw coordinates with proper scaling and positioning."""
        # Scale font size with cell size
        font_size = max(10, int(self.cell_size * 0.15))
        coord_font = ('Helvetica', font_size, 'bold')
        
        # Row numbers (1-6)
        for row in range(6):
            y = self.board_offset_y + (5 - row + 0.5) * self.cell_size
            
            # Left side
            self.canvas.create_text(
                self.border_size * 0.5,
                y,
                text=str(row + 1),
                font=coord_font,
                fill=self.COLORS['coordinate_text'],
                anchor='center'
            )
            
            # Right side
            self.canvas.create_text(
                self.board_offset_x + 5 * self.cell_size + self.border_size * 0.5,
                y,
                text=str(row + 1),
                font=coord_font,
                fill=self.COLORS['coordinate_text'],
                anchor='center'
            )
        
        # Column letters (a-e)
        for col in range(5):
            x = self.board_offset_x + (col + 0.5) * self.cell_size
            
            # Top side
            self.canvas.create_text(
                x,
                self.border_size * 0.5,
                text=chr(97 + col),
                font=coord_font,
                fill=self.COLORS['coordinate_text'],
                anchor='center'
            )
            
            # Bottom side
            self.canvas.create_text(
                x,
                self.board_offset_y + 6 * self.cell_size + self.border_size * 0.5,
                text=chr(97 + col),
                font=coord_font,
                fill=self.COLORS['coordinate_text'],
                anchor='center'
            )

    def draw_pieces(self):
        """Draw pieces with precise positioning."""
        self.canvas.delete('piece')
        self.piece_map.clear()
        
        for row in range(6):
            for col in range(5):
                piece = self.board.get_piece((col, row))
                if piece:
                    x, y = self.get_square_center(col, row)
                    piece_image = self.piece_view.create_piece(piece, x, y)
                    if piece_image:
                        self.piece_map[piece] = piece_image
                        # Ensure piece is centered
                        self.canvas.tag_raise(piece_image)

    def highlight_square(self, col, row, color, alpha=0.3):
        """Highlight square with precise positioning."""
        x1 = self.board_offset_x + col * self.cell_size
        y1 = self.board_offset_y + (5 - row) * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        highlight = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            stipple='gray50',
            tags='highlight',
            alpha=0
        )
        
        self.animate_highlight(highlight, alpha)

    def get_square_from_coords(self, x, y):
        """Convert canvas coordinates to board coordinates with precise border offset."""
        board_x = x - self.board_offset_x
        board_y = y - self.board_offset_y
        
        if board_x < 0 or board_y < 0:
            return None, None
            
        col = int(board_x // self.cell_size)
        row = 5 - int(board_y // self.cell_size)
        
        if col >= 5 or row >= 6 or col < 0 or row < 0:
            return None, None
            
        return col, row

    def animate_piece_movement(self, piece, start_pos, end_pos):
        """Animate piece movement with precise positioning."""
        start_x, start_y = self.get_square_center(*start_pos)
        end_x, end_y = self.get_square_center(*end_pos)
        
        dx = (end_x - start_x) / 10
        dy = (end_y - start_y) / 10
        
        def move_step(steps_left):
            if steps_left > 0:
                self.canvas.move(self.piece_map[piece], dx, dy)
                self.master.after(20, lambda: move_step(steps_left - 1))
            else:
                self.draw_pieces()
        
        move_step(10)