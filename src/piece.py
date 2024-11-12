class Piece:
    def __init__(self, color, position):
        self.color = color  
        self.position = position
        self.has_moved = False

    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        for new_x, new_y in self.generate_moves(board):
            if ignore_check or not board.would_be_in_check(self.color, self.position, (new_x, new_y)):
                moves.append((new_x, new_y))
        return moves

    def is_valid_move(self, board, target_position):
        x, y = target_position
        if not (0 <= x < 5 and 0 <= y < 6):  
            return False
        possible_moves = self.get_possible_moves(board)
        return target_position in possible_moves


class Pawn(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        x, y = self.position
        direction = 1 if self.color == 'white' else -1
        
        # Forward move
        new_y = y + direction
        if 0 <= new_y < 6 and board.board[new_y][x] is None:  # Updated range
            moves.append((x, new_y))
            
        # Capture moves
        for dx in [-1, 1]:
            new_x = x + dx
            if 0 <= new_x < 5 and 0 <= new_y < 6:  # Updated ranges
                target = board.board[new_y][new_x]
                if target and target.color != self.color:
                    moves.append((new_x, new_y))
                    
        return moves

class Rook(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 5 and 0 <= y < 6):  # Updated ranges
                    break
                target = board.board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
                    
        return moves
    
class Knight(Piece):
    def get_possible_moves(self, board, ignore_check=False, ):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        x, y = self.position
        for dx, dy in knight_moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 5 and 0 <= new_y < 6:  # Updated board dimensions
                target = board.board[new_y][new_x]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))
                    
        return moves

class Bishop(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 5 and 0 <= y < 6):  # Updated board dimensions
                    break
                target = board.board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
                    
        return moves

class Queen(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        # Combined rook and bishop movements
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Rook movements
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Bishop movements
        ]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 5 and 0 <= y < 6):  # Updated board dimensions
                    break
                target = board.board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
                    
        return moves

class King(Piece):
    def get_possible_moves(self, board, ignore_check=False):
        moves = []
        # King can move one square in any direction
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Orthogonal moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal moves
        ]
        
        x, y = self.position
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 5 and 0 <= new_y < 6:  # Updated board dimensions
                target = board.board[new_y][new_x]
                if target is None or target.color != self.color:
                    # Check if move would put king in check
                    if ignore_check or not board.would_be_in_check(self.color, (x, y), (new_x, new_y)):
                        moves.append((new_x, new_y))
                        
        return moves
