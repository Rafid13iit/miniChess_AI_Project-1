from .piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        # Changed to 6 rows x 5 columns
        self.board = [[None for _ in range(5)] for _ in range(6)]
        self.initialize_board()

    def initialize_board(self):
        # Initialize pawns
        for x in range(5):
            self.board[1][x] = Pawn('white', (x, 1))
            self.board[4][x] = Pawn('black', (x, 4))

        # Initialize other pieces - removed one bishop
        piece_order = [Rook, Knight, Bishop, Queen, King]
        for x in range(5):
            self.board[0][x] = piece_order[x]('white', (x, 0))
            self.board[5][x] = piece_order[x]('black', (x, 5))

    def move_piece(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        piece = self.board[start_y][start_x]
        if piece and piece.is_valid_move(self, end_pos):
            self.board[end_y][end_x] = piece
            self.board[start_y][start_x] = None
            piece.position = end_pos
            piece.has_moved = True
            return True
        return False

    # In board.py

    def is_in_check(self, color):
        # Locate the king of the specified color
        king_pos = None
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break

        # Check if any opponent piece has a move that can capture the king
        opponent_color = 'black' if color == 'white' else 'white'
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_possible_moves(self, ignore_check=True):
                        return True
        return False


    def would_be_in_check(self, color, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        temp_piece = self.board[end_y][end_x]
        self.board[end_y][end_x] = self.board[start_y][start_x]
        self.board[start_y][start_x] = None
        
        in_check = self.is_in_check(color)
        
        self.board[start_y][start_x] = self.board[end_y][end_x]
        self.board[end_y][end_x] = temp_piece
        
        return in_check

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
            
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    for move in piece.get_possible_moves(self):
                        if not self.would_be_in_check(color, piece.position, move):
                            return False
        return True

    def display(self):
        piece_symbols = {
            Pawn: 'P', Rook: 'R', Knight: 'N',
            Bishop: 'B', Queen: 'Q', King: 'K'
        }
        
        print('  a b c d e')
        print('  ---------')
        for y in range(5, -1, -1):
            row = f"{y+1}|"
            for x in range(5): 
                piece = self.board[y][x]
                if piece is None:
                    row += ' .'
                else:
                    symbol = piece_symbols[type(piece)]
                    if piece.color == 'black':
                        symbol = symbol.lower()
                    row += f' {symbol}'
            print(row)