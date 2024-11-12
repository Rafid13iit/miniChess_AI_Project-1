from .piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        # Initialize the 5x6 board with all None values
        self.board = [[None] * 5 for _ in range(6)]
        
        # Initialize an empty list to store the move history
        self.move_history = []
        
        # Determine whose turn it is. There are only two players in Minichess, so we
        # just switch between 'white' and 'black'.
        self.current_turn = 'white'
        
        # Initialize the board with the starting pieces
        self.initialize_board()


    def initialize_board(self):
        """
        Initialize the board with the starting pieces.

        """
        # Initialize pawns
        # Create a list of 5 pawns for each player, with the correct positions
        # and colors.
        pawns = [Pawn('white', (x, 1)) for x in range(5)]
        # Set the second row of the board to the white pawns.
        self.board[1] = pawns
        # Create a list of 5 pawns for black, with the correct positions and
        # colors.
        self.board[4] = [Pawn('black', (x, 4)) for x in range(5)]
        
        # Initialize other pieces
        # Create a list of pieces for each player, in the order of: Rook, Knight,
        # Bishop, Queen, King.
        piece_order = [Rook, Knight, Bishop, Queen, King]
        # Iterate over the list of pieces, and create an instance of each piece
        # for each player with the correct position and color.
        for x, piece in enumerate(piece_order):
            # Create a white piece at position (x, 0)
            self.board[0][x] = piece('white', (x, 0))
            # Create a black piece at position (x, 5)
            self.board[5][x] = piece('black', (x, 5))

    def get_piece(self, position):
        """
        Get the piece at the specified position on the board.

        :param position: A tuple of two integers, (x, y), that specify the
            position of the piece on the board. The x-coordinate ranges from 0
            to 4, and the y-coordinate ranges from 0 to 5.
        :return: The piece at the specified position, or None if the position is
            empty or out of bounds.
        """
        x, y = position
        # Check that the position is within the board's boundaries
        if 0 <= x < 5 and 0 <= y < 6:
            # If the position is within bounds, then return the piece at that
            # position
            return self.board[y][x]
        # If the position is not within bounds, then return None
        return None

    def is_position_valid(self, position):
        """
        Check if the given position is within the boundaries of the board.

        :param position: A tuple of two integers, (x, y), that specify the
            position of interest on the board.
        :return: A boolean value indicating whether the position is within
            the board's boundaries.
        """
        x, y = position
        # Check that the x-coordinate is within the range 0 to 4
        # The x-coordinate represents the column of the board, and there are
        # 5 columns in a Minichess board.
        is_x_valid = 0 <= x < 5
        # Check that the y-coordinate is within the range 0 to 5
        # The y-coordinate represents the row of the board, and there are
        # 6 rows in a Minichess board.
        is_y_valid = 0 <= y < 6
        # Return True if both coordinates are valid, and False otherwise
        return is_x_valid and is_y_valid

    def is_empty(self, position):
        """Check if the position is empty."""
        return self.get_piece(position) is None

    def get_all_pieces(self, color):
        """
        Get all pieces of specified color.

        This function iterates over the board and checks every position to
        see if there is a piece there. If there is, and the piece is of the
        specified color, then it adds the piece to the list.

        :param color: The color of the pieces to get. This should be a string
            that is either 'white' or 'black'.
        :return: A list of tuples, where each tuple contains a piece and its
            position on the board as a tuple (x, y). The x-coordinate ranges
            from 0 to 4, and the y-coordinate ranges from 0 to 5.
        """
        pieces = []
        for y in range(6):
            for x in range(5):
                # Get the piece at the current position
                piece = self.board[y][x]
                # Check that the piece is not None, and that it is of the
                # specified color.
                if piece and piece.color == color:
                    # If the piece is not None and is of the specified color,
                    # then add it to the list of pieces.
                    pieces.append((piece, (x, y)))
        # Return the list of pieces
        return pieces


    def move_piece(self, start_pos, end_pos):
        """
        Move a piece with full validation and game rules.

        This function is the main entry point for making moves in the game.
        It validates the move, checks if the move would put the king in check,
        captures pieces if present, makes the move, records the move, and then
        switches turns.

        :param start_pos: The starting position of the piece to move, as a
            tuple of two integers, (x, y), where x is the column and y is the
            row of the starting position.
        :param end_pos: The ending position of the piece to move, as a tuple
            of two integers, (x, y), where x is the column and y is the row of
            the ending position.
        :return: A boolean value indicating whether the move was successful.
        """
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        # First, validate the positions. Check that the positions are within
        # the board's boundaries.
        if not (self.is_position_valid(start_pos) and self.is_position_valid(end_pos)):
            # If either position is outside the board, then the move is invalid.
            return False

        # Next, get the piece at the starting position.
        piece = self.board[start_y][start_x]

        # Validate that a piece exists at the starting position, and that it is
        # the correct turn for that piece to move.
        if not piece or piece.color != self.current_turn:
            # If there is no piece at the starting position, or if it is not
            # the correct turn for that piece to move, then the move is invalid.
            return False

        # Check if the move is valid for the piece.
        if not piece.is_valid_move(self, end_pos):
            # If the move is not valid for the piece, then the move is invalid.
            return False

        # Check if the move would put the king in check.
        if self.would_be_in_check(piece.color, start_pos, end_pos):
            # If the move would put the king in check, then the move is invalid.
            return False

        # Capture a piece if one is present at the ending position.
        captured_piece = self.board[end_y][end_x]

        # Make the move.
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None
        piece.position = end_pos
        piece.has_moved = True

        # Record the move.
        self.move_history.append({
            'piece': piece,
            'start': start_pos,
            'end': end_pos,
            'captured': captured_piece
        })

        # Switch turns.
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

        # Finally, return True to indicate that the move was successful.
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
        """
        Determine if the specified color's king is in check.

        This function identifies the position of the king of the specified color
        on the board and checks if any opponent piece can move to that position,
        indicating that the king is in check.

        :param color: The color of the player whose king is being checked.
        :return: True if the king is in check, False otherwise.
        """
        
        # Initialize the king's position
        king_pos = None
        
        # Iterate over the board to find the king of the specified color
        for y in range(6):
            for x in range(5):
                piece = self.board[y][x]
                
                # Check if the piece is a King and matches the specified color
                if isinstance(piece, King) and piece.color == color:
                    # Store the king's position
                    king_pos = (x, y)
                    break
            
            # If the king's position is found, no need to continue the search
            if king_pos:
                break

        # If the king's position is not found, return False (should not occur in a valid game)
        if not king_pos:
            return False

        # Determine the opponent's color
        opponent_color = 'black' if color == 'white' else 'white'
        
        # Check if any opponent piece can move to the king's position
        for piece, pos in self.get_all_pieces(opponent_color):
            # Get all possible moves for the opponent's piece, ignoring checks
            if king_pos in piece.get_possible_moves(self, ignore_check=True):
                # If the king's position is in the possible moves, the king is in check
                return True
        
        # If no opponent piece can capture the king, return False
        return False

    def would_be_in_check(self, color, start_pos, end_pos):
        """
        Check if making a move would result in the player's king being in check.

        This function temporarily makes a move on the board and checks if the move
        would leave the player's king in check. If so, the function returns True,
        indicating that the move is not safe. Otherwise, it returns False.

        :param color: The color of the player making the move.
        :param start_pos: The starting position of the piece to move, as a tuple (x, y).
        :param end_pos: The ending position of the piece to move, as a tuple (x, y).
        :return: A boolean value indicating whether the move would result in check.
        """
        # Unpack the starting and ending positions
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Store the piece being moved and any piece that might be captured
        moving_piece = self.board[start_y][start_x]
        captured_piece = self.board[end_y][end_x]
        
        # Simulate the move by placing the moving piece at the end position
        # and removing it from the start position
        self.board[end_y][end_x] = moving_piece
        self.board[start_y][start_x] = None
        
        # Update the position of the moving piece to the new position
        if moving_piece:
            moving_piece.position = end_pos
        
        # Check if the move would put the player's king in check
        in_check = self.is_in_check(color)
        
        # Restore the board to its original state by moving the piece back
        # and restoring any captured piece
        self.board[start_y][start_x] = moving_piece
        self.board[end_y][end_x] = captured_piece
        
        # Restore the position of the moving piece to its original position
        if moving_piece:
            moving_piece.position = start_pos
        
        # Return whether the move resulted in check
        return in_check

    def is_checkmate(self, color):
        """
        Determine if the specified color is in checkmate.

        A checkmate condition occurs when a player's king is in check and 
        there are no legal moves that the player can make to escape the check.
        
        :param color: The color of the player being checked for checkmate.
        :return: A boolean value indicating whether the player is in checkmate.
        """
        # First, check if the player's king is currently in check.
        # If the king is not in check, then the player cannot be in checkmate.
        if not self.is_in_check(color):
            return False
        
        # Iterate over all pieces of the specified color to find possible moves.
        for piece, pos in self.get_all_pieces(color):
            # For each piece, get all possible moves.
            for move in piece.get_possible_moves(self):
                # Check if making the move would result in the king not being in check.
                if not self.would_be_in_check(color, pos, move):
                    # If any move is found that would prevent the king from being in check,
                    # then the player is not in checkmate.
                    return False
        
        # If no moves can prevent the king from being in check, the player is in checkmate.
        return True

    def is_stalemate(self, color):
        """
        Determine if the specified color is in stalemate.

        A stalemate occurs when a player is not in check, but has no legal moves
        that would not put them in check.
        """
        # First, check if the player is currently in check. If they are, then
        # they are not in stalemate.
        if self.is_in_check(color):
            return False

        # Next, check if any legal moves are available that would not put the
        # player in check. If any such moves are available, then the player is
        # not in stalemate.
        for piece, pos in self.get_all_pieces(color):
            # Iterate over all possible moves for the piece
            for move in piece.get_possible_moves(self):
                # Check if making the move would put the player in check
                if not self.would_be_in_check(color, pos, move):
                    # If the move is legal and would not put the player in check,
                    # then the player is not in stalemate.
                    return False
        # If no legal moves are available that would not put the player in check,
        # then the player is in stalemate.
        return True


    def get_game_state(self):
        """Get the current state of the game."""
        
        # Check if the white player is in checkmate
        if self.is_checkmate('white'):
            # If white is in checkmate, black wins
            return 'Black wins by checkmate'
        
        # Check if the black player is in checkmate
        elif self.is_checkmate('black'):
            # If black is in checkmate, white wins
            return 'White wins by checkmate'
        
        # Check if the game is a stalemate for either player
        elif self.is_stalemate('white') or self.is_stalemate('black'):
            # If either player is in stalemate, the game is a draw
            return 'Draw by stalemate'
        
        # Check if the white player is in check
        elif self.is_in_check('white'):
            # If white is in check but not checkmate, return that white is in check
            return 'White is in check'
        
        # Check if the black player is in check
        elif self.is_in_check('black'):
            # If black is in check but not checkmate, return that black is in check
            return 'Black is in check'
        
        else:
            # If none of the above conditions are met, return the current player's turn
            return f"{self.current_turn.capitalize()}'s turn"

    def display(self):
        """Display the current state of the board."""
        
        # Define the symbols used to represent each piece type on the board
        piece_symbols = {
            Pawn: 'P', Rook: 'R', Knight: 'N',
            Bishop: 'B', Queen: 'Q', King: 'K'
        }
        
        # Print the column headers for the board
        print('\n  a b c d e')
        print('  ---------')
        
        # Iterate over each row of the board from top to bottom (5 to 0)
        for y in range(5, -1, -1):
            # Start the row string with the row number and a separator
            row = f"{y+1}|"
            
            # Iterate over each column of the board from left to right (0 to 4)
            for x in range(5):
                # Get the piece at the current position
                piece = self.board[y][x]
                
                # If there's no piece, add a dot to represent an empty square
                if piece is None:
                    row += ' .'
                else:
                    # Get the symbol for the piece type
                    symbol = piece_symbols[type(piece)]
                    
                    # If the piece is black, use a lowercase symbol
                    if piece.color == 'black':
                        symbol = symbol.lower()
                    
                    # Add the piece symbol to the row string
                    row += f' {symbol}'
            
            # Print the completed row with piece symbols
            print(row)
        
        # Print the current game state message
        print(f"\n{self.get_game_state()}")
