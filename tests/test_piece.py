import unittest
from src.board import Board
from src.piece import Pawn, Knight

class TestPiece(unittest.TestCase):
    def setUp(self):
        self.board = Board()
    
    def test_knight_moves(self):
        knight = self.board.board[0][1]  # White knight
        moves = knight.get_possible_moves(self.board)
        # In 6x5 board, knight at (1,0) can move to (0,2) and (2,2)
        expected_moves = [(0, 2), (2, 2)]
        for move in expected_moves:
            self.assertIn(move, moves)
    
    def test_bishop_moves(self):
        # Clear some pawns to test bishop movement
        self.board.board[1][1] = None  # Remove pawn in front of bishop
        bishop = self.board.board[0][2]  # White bishop
        moves = bishop.get_possible_moves(self.board)
        # Bishop should be able to move diagonally
        expected_moves = [(1, 1), (3, 3)]  # Example diagonal moves
        for move in expected_moves:
            self.assertIn(move, moves)
    
    def test_queen_moves(self):
        # Clear some pawns to test queen movement
        self.board.board[1][3] = None  # Remove pawn in front of queen
        queen = self.board.board[0][3]  # White queen
        moves = queen.get_possible_moves(self.board)
        # Queen should be able to move vertically and diagonally
        expected_moves = [(3, 1), (3, 2)]  # Example vertical moves
        for move in expected_moves:
            self.assertIn(move, moves)
    
    def test_king_moves(self):
        # Clear some pawns to test king movement
        self.board.board[1][4] = None  # Remove pawn in front of king
        king = self.board.board[0][4]  # White king
        moves = king.get_possible_moves(self.board)
        # King should be able to move one square in any direction
        expected_moves = [(4, 1), (3, 1)]  # Example moves
        for move in expected_moves:
            self.assertIn(move, moves)