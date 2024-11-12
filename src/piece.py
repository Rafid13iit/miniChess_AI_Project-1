class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position
        self.has_moved = False

    def get_possible_moves(self, board, ignore_check=False):
        """
        Returns a list of possible moves for this piece.

        This function works by first generating all possible moves for this piece
        (ignoring the check constraint). It then checks each of the moves to see
        if it would put the piece in check. If not, it adds the move to the list
        of possible moves.

        If ignore_check is True, then the check constraint is ignored and all
        possible moves are returned.
        """
        moves = []
        for new_x, new_y in self.generate_moves(board):
            # Check if the move would put the piece in check
            if ignore_check or not board.would_be_in_check(self.color, self.position, (new_x, new_y)):
                # If not, add the move to the list of possible moves
                moves.append((new_x, new_y))
        return moves

    def is_valid_move(self, board, target_position):
        """
        Check if a move is valid for this piece.

        A move is valid if the target position is within the board's boundaries
        and if the target position is in the list of possible moves for this
        piece.

        :param board: The board object
        :param target_position: The target position to check, as a tuple (x, y)
        :return: A boolean value indicating whether the move is valid
        """
        x, y = target_position
        if not (0 <= x < 5 and 0 <= y < 6):  # Updated board boundaries
            # If the target position is outside the board's boundaries, then
            # the move is invalid
            return False
        possible_moves = self.get_possible_moves(board)
        # Check if the target position is in the list of possible moves
        return target_position in possible_moves


class Pawn(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        """
        Get all possible moves for the Pawn.

        The Pawn moves forward one square, but captures diagonally one square.
        The method iterates over all possible moves and checks if the move is
        valid according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the Pawn in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the Pawn in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the Pawn in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        x, y = self.position  # Get the current position of the Pawn
        direction = 1 if self.color == 'white' else -1  # Determine the direction of the Pawn's move
        
        # Check if the Pawn can move forward one square
        new_y = y + direction
        if 0 <= new_y < 6 and board.board[new_y][x] is None:  # Check if the new position is within the board's boundaries and if the target position is empty
            # If the move is valid, add it to the list of moves
            moves.append((x, new_y))
            
        # Check if the Pawn can capture diagonally one square
        for dx in [-1, 1]:  # Iterate over the two possible diagonal moves
            new_x = x + dx
            if 0 <= new_x < 5 and 0 <= new_y < 6:  # Check if the new position is within the board's boundaries
                target = board.board[new_y][new_x]  # Get the piece at the target position
                if target and target.color != self.color:  # Check if the target position is occupied by a piece of the opposite color
                    # If the move is valid, add it to the list of moves
                    moves.append((new_x, new_y))
                    
        # Return the list of moves
        return moves

class Rook(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        """
        Get all possible moves for the Rook.

        The Rook moves horizontally or vertically any number of squares. The
        method iterates over all possible moves and checks if the move is valid
        according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the Rook in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the Rook in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the Rook in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # Iterate over all possible directions
        for dx, dy in directions:
            x, y = self.position
            # Keep moving in this direction until we reach the edge of the board
            while True:
                x += dx
                y += dy
                # Check if we are still within the board's boundaries
                if not (0 <= x < 5 and 0 <= y < 6):  # Updated ranges
                    # If we are not, then break out of this loop
                    break
                # Get the piece at the target position
                target = board.board[y][x]
                # Check if the target position is empty
                if target is None:
                    # If it is, then add the move to the list of possible moves
                    moves.append((x, y))
                # Check if the target position is occupied by a piece of the
                # opposite color
                elif target.color != self.color:
                    # If it is, then add the move to the list of possible moves
                    moves.append((x, y))
                    # And break out of this loop, since we can't move any further
                    # in this direction
                    break
                else:
                    # If the target position is occupied by a piece of the same
                    # color, then break out of this loop, since we can't move
                    # any further in this direction
                    break
                    
        # Return the list of possible moves
        return moves
    
class Knight(Piece):
    def get_possible_moves(self, board, ignore_check=False, ):
        """
        Get all possible moves for the Knight.

        The Knight moves in an L-shape, two squares in one direction and one
        square in a perpendicular direction. The method calculates all possible
        moves for the Knight by iterating over all possible directions and
        checking if the move is valid according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the King in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the Knight in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the Knight in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        # Define all possible moves for the Knight
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        x, y = self.position
        # Iterate over all possible directions
        for dx, dy in knight_moves:
            # Calculate the new position of the Knight if it were to move in
            # this direction
            new_x, new_y = x + dx, y + dy
            # Check if the new position is within the board's boundaries
            if 0 <= new_x < 5 and 0 <= new_y < 6:  # Updated board dimensions
                # Get the piece at the new position
                target = board.board[new_y][new_x]
                # Check if the move is valid according to the rules above
                if target is None or target.color != self.color:
                    # If the move is valid, add it to the list of moves
                    moves.append((new_x, new_y))
                    
        # Return the list of moves
        return moves

class Bishop(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        """
        Get all possible moves for the Bishop.

        The Bishop can move any number of squares in any diagonal direction.
        The method iterates over all possible moves and checks if the move is
        valid according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the Bishop in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the Bishop in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the Bishop in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        # Define the possible moves for the Bishop
        directions = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal movements
        ]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 5 and 0 <= y < 6):  # Check if the move is
                    # within the board's boundaries
                    break
                target = board.board[y][x]
                if target is None:
                    # If the target square is empty, add the move to the list
                    # of possible moves
                    moves.append((x, y))
                elif target.color != self.color:
                    # If the target square is occupied by a piece of the opposite
                    # color, add the move to the list of possible moves
                    moves.append((x, y))
                    break
                else:
                    # If the target square is occupied by a piece of the same
                    # color, then the move is invalid
                    break
                    
        return moves

class Queen(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        """
        Get all possible moves for the Queen.

        The Queen can move any number of squares in any direction (orthogonal or
        diagonal). The method iterates over all possible moves and checks if the
        move is valid according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the Queen in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the Queen in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the Queen in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        # Define the possible moves for the Queen
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Rook movements
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Bishop movements
        ]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                # Move the Queen in the current direction
                x += dx
                y += dy
                
                # Check if the move is within the board's boundaries
                if not (0 <= x < 5 and 0 <= y < 6):  # Updated board dimensions
                    break
                
                # Get the piece at the target position
                target = board.board[y][x]
                
                # Check if the move is valid
                if target is None:
                    # If the target position is empty, add the move to the list of
                    # possible moves
                    moves.append((x, y))
                elif target.color != self.color:
                    # If the target position is occupied by a piece of the opposite
                    # color, add the move to the list of possible moves and break
                    # out of the loop
                    moves.append((x, y))
                    break
                else:
                    # If the target position is occupied by a piece of the same
                    # color, break out of the loop
                    break
                    
        return moves

class King(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        """
        Get all possible moves for the King.

        The King can move one square in any direction (orthogonal or diagonal).
        The method iterates over all possible moves and checks if the move is
        valid according to the following rules:

        1. The move must be within the board's boundaries.
        2. The move cannot be to a square that is occupied by another piece of
           the same color.
        3. The move cannot put the King in check.

        If the 'ignore_check' parameter is set to True, the method will not
        check if the move would put the King in check.

        :param board: The current game board.
        :param ignore_check: A boolean value indicating whether to ignore
            checking if the move would put the King in check.
        :return: A list of tuples, where each tuple contains the x-coordinate
            and y-coordinate of a possible move.
        """
        moves = []
        # Define the possible moves for the King
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Orthogonal moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal moves
        ]
        
        x, y = self.position
        for dx, dy in directions:
            # Calculate the new position of the King if it were to move in this
            # direction
            new_x, new_y = x + dx, y + dy
            # Check if the new position is within the board's boundaries
            if 0 <= new_x < 5 and 0 <= new_y < 6:
                # Get the piece at the new position
                target = board.board[new_y][new_x]
                # Check if the move is valid according to the rules above
                if target is None or target.color != self.color:
                    # Check if the move would put the King in check
                    if ignore_check or not board.would_be_in_check(self.color, (x, y), (new_x, new_y)):
                        # If the move is valid, add it to the list of moves
                        moves.append((new_x, new_y))
                        
        return moves

