import random
from copy import deepcopy
from .board import Board
from .piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class MinichessAI:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def evaluate_board(self, board):
        piece_values = {
            Pawn: 100,
            Knight: 320,
            Bishop: 330,
            Rook: 500,
            Queen: 900,
            King: 20000
        }
        
        score = 0
        for row in range(6):  # 6 rows
            for col in range(5):  # 5 columns
                piece = board.get_piece((col, row))
                if piece:
                    value = piece_values.get(type(piece), 0)  # Safely get piece value
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value
        
        # Add bonus points for controlling the center
        center_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]
        for pos in center_positions:
            piece = board.get_piece(pos)
            if piece and piece.color == self.color:
                score += 50
            elif piece and piece.color != self.color:
                score -= 50
        
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_checkmate(self.color) or board.is_stalemate(self.color):
            return self.evaluate_board(board)
            
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(board, self.color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_color = 'black' if self.color == 'white' else 'white'
            for move in self.get_all_moves(board, opponent_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_all_moves(self, board, color):
        moves = []
        pieces = board.get_all_pieces(color)
        for piece, pos in pieces:
            for move in piece.get_possible_moves(board):
                if not board.would_be_in_check(color, pos, move):
                    moves.append((pos, move))
        return moves


    def get_best_move(self, board):
        best_move = None
        best_eval = float('-inf')
        
        for move in self.get_all_moves(board, self.color):
            new_board = deepcopy(board)
            new_board.move_piece(move[0], move[1])
            eval = self.minimax(new_board, self.depth - 1, best_eval, float('inf'), False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
                
        return best_move
