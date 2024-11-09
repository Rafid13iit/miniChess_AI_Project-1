from .piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = [[None] * 5 for _ in range(6)]
        self.move_history = []
        self.current_turn = 'white'
        self.initialize_board()


    def initialize_board(self):
        # Initialize pawns
        pawns = [Pawn('white', (x, 1)) for x in range(5)]
        self.board[1] = pawns
        self.board[4] = [Pawn('black', (x, 4)) for x in range(5)]

        # Initialize other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King]
        for x, piece in enumerate(piece_order):
            self.board[0][x] = piece('white', (x, 0))
            self.board[5][x] = piece('black', (x, 5))

    def get_piece(self, position):
        """Get piece at the specified position."""
        x, y = position
        if 0 <= x < 5 and 0 <= y < 6:
            return self.board[y][x]
        return None

    def is_position_valid(self, position):
        """Check if the position is within board boundaries."""
        x, y = position
        return 0 <= x < 5 and 0 <= y < 6

    def is_empty(self, position):
        """Check if the position is empty."""
        return self.get_piece(position) is None

    def get_all_pieces(self, color):
        """Get all pieces of specified color."""
        pieces = []
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    pieces.append((piece, (x, y)))
        return pieces

    def move_piece(self, start_pos, end_pos):
        """Move a piece with full validation and game rules."""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Basic validation
        if not (self.is_position_valid(start_pos) and self.is_position_valid(end_pos)):
            return False
            
        piece = self.board[start_y][start_x]
        
        # Validate piece existence and turn
        if not piece or piece.color != self.current_turn:
            return False
            
        # Check if move is valid for the piece
        if not piece.is_valid_move(self, end_pos):
            return False
            
        # Check if move would put/leave king in check
        if self.would_be_in_check(piece.color, start_pos, end_pos):
            return False
            
        # Capture piece if present
        captured_piece = self.board[end_y][end_x]
        
        # Make the move
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None
        piece.position = end_pos
        piece.has_moved = True
        
        # Record the move
        self.move_history.append({
            'piece': piece,
            'start': start_pos,
            'end': end_pos,
            'captured': captured_piece
        })
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        return True

    def undo_last_move(self):
        """Undo the last move made."""
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        piece, start_pos, end_pos, captured_piece = (
            last_move['piece'],
            last_move['start'],
            last_move['end'],
            last_move['captured'],
        )

        # Restore piece to original position
        self.board[start_pos[1]][start_pos[0]], self.board[end_pos[1]][end_pos[0]] = piece, captured_piece
        piece.position = start_pos

        # Switch turns back
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

        return True

    def is_in_check(self, color):
        """Determine if the specified color's king is in check."""
        # Find king position
        king_pos = None
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break

        if not king_pos:
            return False  # Should not happen in a valid game

        # Check if any opponent piece can capture the king
        opponent_color = 'black' if color == 'white' else 'white'
        for piece, pos in self.get_all_pieces(opponent_color):
            if king_pos in piece.get_possible_moves(self, ignore_check=True):
                return True
        return False

    def would_be_in_check(self, color, start_pos, end_pos):
        """Check if making a move would result in check."""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Store pieces for restoration
        moving_piece = self.board[start_y][start_x]
        captured_piece = self.board[end_y][end_x]
        
        # Make temporary move
        self.board[end_y][end_x] = moving_piece
        self.board[start_y][start_x] = None
        if moving_piece:
            moving_piece.position = end_pos
        
        # Check if king is in check
        in_check = self.is_in_check(color)
        
        # Restore board
        self.board[start_y][start_x] = moving_piece
        self.board[end_y][end_x] = captured_piece
        if moving_piece:
            moving_piece.position = start_pos
        
        return in_check

    def is_checkmate(self, color):
        """Determine if the specified color is in checkmate."""
        if not self.is_in_check(color):
            return False
            
        # Check all possible moves for all pieces
        for piece, pos in self.get_all_pieces(color):
            for move in piece.get_possible_moves(self):
                if not self.would_be_in_check(color, pos, move):
                    return False
        return True

    def is_stalemate(self, color):
        """Determine if the specified color is in stalemate."""
        if self.is_in_check(color):
            return False
            
        # Check if any legal moves are available
        for piece, pos in self.get_all_pieces(color):
            for move in piece.get_possible_moves(self):
                if not self.would_be_in_check(color, pos, move):
                    return False
        return True

    def get_game_state(self):
        """Get the current state of the game."""
        if self.is_checkmate('white'):
            return 'Black wins by checkmate'
        elif self.is_checkmate('black'):
            return 'White wins by checkmate'
        elif self.is_stalemate('white') or self.is_stalemate('black'):
            return 'Draw by stalemate'
        elif self.is_in_check('white'):
            return 'White is in check'
        elif self.is_in_check('black'):
            return 'Black is in check'
        else:
            return f"{self.current_turn.capitalize()}'s turn"

    def display(self):
        """Display the current state of the board."""
        piece_symbols = {
            Pawn: 'P', Rook: 'R', Knight: 'N',
            Bishop: 'B', Queen: 'Q', King: 'K'
        }
        
        print('\n  a b c d e')
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
        print(f"\n{self.get_game_state()}")