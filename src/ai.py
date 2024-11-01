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
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 100
        }
        
        score = 0
        for y in range(6):  # 6 rows
            for x in range(5):  # 5 columns
                piece = board.board[y][x]
                if piece:
                    value = piece_values.get(type(piece), 0)  # Safely get piece value
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value
        
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
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
        for y in range(6):  # 6 rows
            for x in range(5):  # 5 columns
                piece = board.board[y][x]
                if piece and piece.color == color:
                    for move in piece.get_possible_moves(board):
                        moves.append((piece.position, move))
        return moves

    def get_best_move(self, board):
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.get_all_moves(board, self.color):
            new_board = deepcopy(board)
            new_board.move_piece(move[0], move[1])
            eval = self.minimax(new_board, self.depth - 1, alpha, beta, False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
                
        return best_move
