from chess.components import Coordinate, Color, Board
from chess.game.player import Player
from chess.pieces.piece_abc import Piece, PieceType
from chess.pieces.pawn import Pawn

class Queen(Piece):
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.QUEEN

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the queen.
		"""
		moves: list[Coordinate] = []

		# directions in comments are from white's perspective
		attacking_directions: list[tuple[int, int]] = [
			(0, 1), # up
			(0, -1), # down
			(1, 0), # right
			(-1, 0), # left
			(1, 1), # up&right
			(-1, -1), # down&left
			(1, -1), # up&left
			(-1, 1), # down&right
		]

		for direction in attacking_directions:
			moves.extend(
				self.board.get_coordinates(self.coordinate, direction)
			)

		return moves


	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the queen can choose.
		regardless of checks.
		"""

		return super().available_moves()

	def __repr__(self):
		return 'Q' if self.color == Color.WHITE else 'q'

def main():
	b = Board()

	q = Queen(b, Color.WHITE, Coordinate('e4'))
	Pawn(b, Color.WHITE, Coordinate('f3'))

	print(b)
	print(q.attacking_coordinates())
	print(q.available_moves())

if __name__ == '__main__':
	main()