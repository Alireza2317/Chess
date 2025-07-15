import unittest
from chess.engine.core import Coordinate
from chess.engine.pieces.pawn import Pawn
from chess.game.game import Game

class TestGameBasics(unittest.TestCase):
	def setUp(self) -> None:
		self.game = Game()
		self.white = self.game.white
		self.black = self.game.black
		self.board = self.game.board

	def test_initial_pawn_moves(self) -> None:
		# place white pawn on e2
		pawn = Pawn(self.white, Coordinate('e', '2'))

		self.white.update_legal_moves()

		expected_moves = {Coordinate('e', '3'), Coordinate('e', '4')}
		self.assertEqual(pawn.legal_moves, expected_moves)

	def test_move_execution(self) -> None:
		pawn = Pawn(self.white, Coordinate('d', '2'))

		self.white.update_legal_moves()
		success = self.game.move(Coordinate('d', '2'), Coordinate('d', '4'))
		self.assertTrue(success)

		new_pos = self.board[Coordinate('d', '4')].piece
		self.assertIs(new_pos, pawn)
		self.assertEqual(pawn.coordinate, Coordinate('d', '4'))

	def test_illegal_move(self) -> None:
		pawn = Pawn(self.white, Coordinate('a', '2'))

		self.white.update_legal_moves()
		success = self.game.move(Coordinate('a', '2'), Coordinate('a', '5'))
		self.assertFalse(success)


if __name__ == '__main__':
	unittest.main()
