import unittest
from src.board import Board
from src.ai import MinichessAI

class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.ai = MinichessAI('white', depth=2)

    def test_evaluate_board(self):
        score = self.ai.evaluate_board(self.board)
        self.assertEqual(score, 0)  

    def test_get_best_move(self):
        move = self.ai.get_best_move(self.board)
        self.assertIsNotNone(move)
        self.assertEqual(len(move), 2)  