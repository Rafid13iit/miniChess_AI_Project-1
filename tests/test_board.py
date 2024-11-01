import unittest
from src.board import Board
from src.piece import Pawn, Rook, Knight, Bishop, Queen, King

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        # Test pawns
        for x in range(5):  # Updated range
            self.assertIsInstance(self.board.board[1][x], Pawn)
            self.assertEqual(self.board.board[1][x].color, 'white')
            self.assertIsInstance(self.board.board[4][x], Pawn)
            self.assertEqual(self.board.board[4][x].color, 'black')

        # Test other pieces
        piece_types = [Rook, Knight, Bishop, Queen, King]  # Removed one bishop
        for x in range(5):  # Updated range
            self.assertIsInstance(self.board.board[0][x], piece_types[x])
            self.assertEqual(self.board.board[0][x].color, 'white')
            self.assertIsInstance(self.board.board[5][x], piece_types[x])
            self.assertEqual(self.board.board[5][x].color, 'black')

    def test_move_piece(self):
        # Test pawn move
        self.assertTrue(self.board.move_piece((0, 1), (0, 2)))
        self.assertIsInstance(self.board.board[2][0], Pawn)
        self.assertIsNone(self.board.board[1][0])

    def test_invalid_move(self):
        # Test invalid pawn move
        self.assertFalse(self.board.move_piece((0, 1), (0, 3)))