import random
from copy import deepcopy
from .board import Board
from .piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class MinichessAI:
    def __init__(self, color, depth=3):
        """
        Initialize a Minichess AI with color and depth.

        Parameters:
            color (str): The color of the AI, either 'white' or 'black'.
            depth (int): The depth the AI should search. Defaults to 3.
        """
        self.color = color
        self.depth = depth

    def evaluate_board(self, board):
        """
        Evaluate the given board from the AI's perspective.

        The evaluation is based on the total value of all pieces on the board, with higher values for more powerful pieces.
        The AI also gains points for controlling the center of the board, which is a strategic advantage.

        Returns an integer score representing the evaluation. Higher scores are better for the AI.
        """
        # Piece values are based on their relative strengths. The King is worth the most, as it is the most important piece.
        # The values are based on the relative strengths of each piece, with higher values meaning the piece is more powerful.
        # The values are also based on the fact that the AI is trying to maximize its score, so pieces that are more difficult to use are worth less.
        piece_values = {
            Pawn: 100,  # Pawns are weak, but can be promoted to more powerful pieces
            Knight: 320,  # Knights are somewhat powerful, but can be tricky to use
            Bishop: 330,  # Bishops are somewhat powerful, and are good at controlling the diagonals
            Rook: 500,  # Rooks are powerful, and are good at controlling the ranks and files
            Queen: 900,  # The Queen is very powerful, and can control the entire board
            King: 20000  # The King is the most important piece, and is worth a lot of points
        }
        
        # Initialize the score to 0
        score = 0

        # Iterate over all positions on the board
        for row in range(6):  # 6 rows
            for col in range(5):  # 5 columns
                piece = board.get_piece((col, row))
                if piece:
                    # Get the value of the piece from the piece_values dictionary
                    value = piece_values.get(type(piece), 0)
                    # If the piece is the AI's color, add its value to the score
                    if piece.color == self.color:
                        score += value
                    # If the piece is the opponent's color, subtract its value from the score
                    else:
                        score -= value

        # Add bonus points for controlling the center
        center_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]
        for pos in center_positions:
            piece = board.get_piece(pos)
            # If the AI controls the center position, add 50 points to the score
            if piece and piece.color == self.color:
                score += 50
            # If the opponent controls the center position, subtract 50 points from the score
            elif piece and piece.color != self.color:
                score -= 50

        # Return the final score
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Perform the Minimax algorithm to find the best move for the AI.

        The Minimax algorithm is a recursive algorithm used to find the best move in a game tree. It works by
        evaluating all possible moves and their outcomes, and then choosing the best move based on the evaluation.

        Parameters:
            board (Board): The current state of the board.
            depth (int): The current depth of the search. The search will stop when the depth reaches 0.
            alpha (int): The best possible score for the maximizing player (the AI). Used to prune the search tree.
            beta (int): The best possible score for the minimizing player (the opponent). Used to prune the search tree.
            maximizing_player (bool): Whether the AI is the maximizing player (True) or the minimizing player (False).

        Returns the best possible score for the AI.
        """
        # If the depth is 0, or if the game is over, return the evaluation of the current board
        if depth == 0 or board.is_checkmate(self.color) or board.is_stalemate(self.color):
            return self.evaluate_board(board)

        # If the AI is the maximizing player, try to find the best move that maximizes the score
        if maximizing_player:
            # Initialize the maximum evaluation to negative infinity
            max_eval = float('-inf')

            # Iterate over all possible moves for the AI
            for move in self.get_all_moves(board, self.color):
                # Create a new board with the move applied
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])

                # Recursively call the Minimax algorithm to find the best move for the opponent
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)

                # Update the maximum evaluation if the current evaluation is better
                max_eval = max(max_eval, eval)

                # Update alpha (the best possible score for the AI) if the current evaluation is better
                alpha = max(alpha, eval)

                # If beta (the best possible score for the opponent) is less than or equal to alpha, prune the search tree
                if beta <= alpha:
                    break

            # Return the maximum evaluation
            return max_eval

        # If the AI is the minimizing player, try to find the best move that minimizes the score
        else:
            # Initialize the minimum evaluation to positive infinity
            min_eval = float('inf')

            # Iterate over all possible moves for the opponent
            opponent_color = 'black' if self.color == 'white' else 'white'
            for move in self.get_all_moves(board, opponent_color):
                # Create a new board with the move applied
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])

                # Recursively call the Minimax algorithm to find the best move for the AI
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)

                # Update the minimum evaluation if the current evaluation is better
                min_eval = min(min_eval, eval)

                # Update beta (the best possible score for the opponent) if the current evaluation is better
                beta = min(beta, eval)

                # If alpha (the best possible score for the AI) is less than or equal to beta, prune the search tree
                if beta <= alpha:
                    break

            # Return the minimum evaluation
            return min_eval

    def get_all_moves(self, board, color):
        """
        Get all possible moves for the specified color.

        :param board: The current game board.
        :param color: The color of the pieces to get moves for ('white' or 'black').
        :return: A list of tuples, where each tuple contains the starting position and ending position of the move.
        """
        moves = []

        # Get all pieces of the specified color
        pieces = board.get_all_pieces(color)

        # Iterate over each piece
        for piece, pos in pieces:
            # Get all possible moves for the piece
            for move in piece.get_possible_moves(board):
                # Check if the move would put the king in check
                if not board.would_be_in_check(color, pos, move):
                    # If not, add the move to the list of moves
                    moves.append((pos, move))

        # Return the list of moves
        return moves


    def get_best_move(self, board):
        # Initialize the best move as None and the best evaluation score as negative infinity
        best_move = None
        best_eval = float('-inf')
        
        # Iterate over all possible moves for the AI
        for move in self.get_all_moves(board, self.color):
            # Create a deep copy of the board to simulate the move
            new_board = deepcopy(board)
            # Apply the move to the new board
            new_board.move_piece(move[0], move[1])
            # Use the Minimax algorithm to evaluate the move
            eval = self.minimax(new_board, self.depth - 1, best_eval, float('inf'), False)
            # If the evaluation of the move is better than the current best evaluation
            if eval > best_eval:
                # Update the best evaluation and the best move
                best_eval = eval
                best_move = move
                
        # Return the move with the highest evaluation score
        return best_move
